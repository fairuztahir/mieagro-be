import os
import asyncpg
import aioredis

from contextvars import ContextVar
from sanic import Sanic, Blueprint
from sanic.log import logger
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, insert

from views.user import UserController
from views.role import RoleController
from views.auth import AuthController
from views.odoo import OdooController
from views.warehouse import WarehouseController
from views.product import ProductController
from views.uploads import FileController
from views.attribute import AttributeController
from views.attribute_value import AttributeValueController
from views.product_attribute_line import ProductAttributeLineController
from views.product_attribute_value import ProductAttributeValueController
from utils.exportcsv import DownloadCSVView
from utils.scheduler import main, stop
from models.base import Base
from models.role import Role
from models.user import User
from helpers.func import make_hash, createUploadPath, valueOf
from helpers.seeds.main import userSeed, roleSeed


def create(*args, **kwargs):
    app = Sanic(*args, **kwargs)
    before_server_start(app)
    after_server_start(app)
    after_server_stop(app)
    add_middleware(app)
    init_blueprints(app)
    return app


def before_server_start(app):
    @app.listener('before_server_start')
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


def after_server_start(app):
    @app.listener('after_server_start')
    async def create_task_queue(app, loop):
        app.config["UPLOAD_DIR"] = valueOf.UPLOAD_DIR.fulltext
        await main(app, loop)
        await createUploadPath(app)


def after_server_stop(app):
    @app.listener('after_server_stop')
    async def run(app, loop):
        await stop()
        await app.ctx.db.dispose()
        await app.ctx.redis.disconnect()


def init_blueprints(app):
    v1_0 = Blueprint.group(
        AuthController.a,
        UserController.u,
        RoleController.r,
        WarehouseController.wh,
        ProductController.p,
        OdooController.o,
        DownloadCSVView.c,
        FileController.f,
        AttributeController.p,
        AttributeValueController.p,
        ProductAttributeLineController.p,
        ProductAttributeValueController.p,
        url_prefix='/',
        version=1
    )
    app.blueprint(v1_0)


async def redis_pool(app):
    # MARK: using aioredis > v2 https://aioredis.readthedocs.io/en/latest/examples/#pubsub
    app.ctx.redis = aioredis.ConnectionPool.from_url(
        "redis://redis:6379", encoding="utf-8", decode_responses=True
    )
    meanings = aioredis.Redis(connection_pool=app.ctx.redis)
    try:
        await meanings.set("life", 42)
        print(f"Test Redis: {await meanings.get('life')}")
        await meanings.delete("life")
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
