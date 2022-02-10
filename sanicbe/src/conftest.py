import pytest
import os
import sys
import asyncpg
import aioredis

from contextvars import ContextVar
from sanic import Sanic, Blueprint, response
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, insert

from views.user import UserController
from views.role import RoleController
from views.auth import AuthController
from views.uploads import FileController
from utils.exportcsv import DownloadCSVView
from models.base import Base
from models.role import Role
from models.user import User
from helpers.func import make_hash
from helpers.seeds.main import userSeed, roleSeed


sys.dont_write_bytecode = True


@pytest.fixture
def app():
    sanic_app = create('test_api')

    @sanic_app.get("/ping")
    async def ping_test(request):
        return response.json({"message": "pong!"})

    return sanic_app


def create(*args, **kwargs):
    app = Sanic(*args, **kwargs)
    after_server_start(app)
    before_server_stop(app)
    add_middleware(app)
    init_blueprints(app)
    return app


def after_server_start(app):
    @app.listener('after_server_start')
    async def run(app, loop):
        dsn = "postgresql+asyncpg://{user}:{pwd}@{host}:5432/{database}".format(
            user=os.getenv('POSTGRES_USER', 'postgres'),
            pwd=os.getenv('POSTGRES_PASSWORD', 'postgres'),
            host=os.getenv('POSTGRES_HOST', 'localhost'),
            database=os.getenv('POSTGRES_DB', 'postgres')
        )
        debug_mode = os.getenv('APP_ENV', '') == 'dev'
        app.ctx.db = create_async_engine(dsn, echo=debug_mode)
        await redis_pool(app)
        await db_migrate(app)


def before_server_stop(app):
    @app.listener('before_server_stop')
    async def run(app, loop):
        await app.ctx.db.dispose()
        await app.ctx.redis.disconnect()


def init_blueprints(app):
    v1_0 = Blueprint.group(
        AuthController.a,
        UserController.u,
        RoleController.r,
        DownloadCSVView.c,
        FileController.f,
        url_prefix='/',
        version=1
    )
    app.blueprint(v1_0)


async def redis_pool(app):
    app.ctx.redis = aioredis.ConnectionPool.from_url(
        "redis://redis:6379", encoding="utf-8", decode_responses=True
    )
    meanings = aioredis.Redis(connection_pool=app.ctx.redis)
    try:
        await meanings.set("life", 42)
        print(f"The answer: {await meanings.get('life')}")
    finally:
        await app.ctx.redis.disconnect()


async def db_migrate(app):
    async with app.ctx.db.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with app.ctx.db.connect() as conn:
        stmt = select(Role.id).where(Role.name == 'Admin')
        data = await conn.execute(stmt)
        if not data.scalar():
            await conn.execute(insert(Role), roleSeed)
            await conn.commit()

            stmt = select(Role.id).where(Role.name == 'Admin')
            data = await conn.execute(stmt)
            challenge = str(os.getenv('API_ADMIN_PASSWORD', 'admin'))
            hashed = await make_hash(challenge)
            email = str(os.getenv('API_ADMIN_EMAIL', 'admin@gmail.com'))
            userSeed[0]["email"] = email
            userSeed[0]["challenge"] = hashed
            userSeed[0]["role_id"] = data.scalar()
            await conn.execute(insert(User), userSeed)
            await conn.commit()
        await conn.close()


async def drop_db(app):
    async with app.ctx.db.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


def add_middleware(app):
    app.config.SECRET = os.getenv('JWT_SECRET', 'secret')
    _base_model_session_ctx = ContextVar("session")

    @app.middleware("request")
    async def inject_session(request):
        request.ctx.session = sessionmaker(
            app.ctx.db, AsyncSession, expire_on_commit=False)()
        request.ctx.session_ctx_token = _base_model_session_ctx.set(
            request.ctx.session)

    @app.middleware("response")
    async def close_session(request, response):
        if hasattr(request.ctx, "session_ctx_token"):
            _base_model_session_ctx.reset(request.ctx.session_ctx_token)
            await request.ctx.session.close()
