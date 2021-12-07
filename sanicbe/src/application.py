import os
import asyncpg
import aioredis

from contextvars import ContextVar
from sanic import Sanic, Blueprint, views
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
from utils.exportcsv import DownloadCSVView
from utils.scheduler import main, stop
from models.base import Base
from models.role import Role
from models.user import User
from helpers.func import make_hash, createUploadPath, valueOf


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
        app.db = create_async_engine(dsn, echo=debug_mode)
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
        await app.db.dispose()
        app.redis.close()
        await app.redis.wait_closed()


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
        url_prefix='/',
        version=1
    )
    app.blueprint(v1_0)


async def redis_pool(app):
    # MARK: using aioredis v1.3.1, got bug with v2.0.0 and need to downgrade python 3.10 to 3.9
    app.redis = await aioredis.create_redis_pool('redis://redis:6379', encoding='utf-8', maxsize=10)
    # await app.redis.set('my-key', 'value')
    # val = await app.redis.get('my-key')
    # print('raw value:', val)


async def db_migrate(app):
    async with app.db.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with app.db.connect() as conn:
        stmt = select(Role.id).where(Role.name == 'Admin')
        data = await conn.execute(stmt)
        if not data.scalar():
            await conn.execute(insert(Role), [
                {"name": "Admin", "description": "Admin role setting with all privileges."},
                {"name": "User", "description": "User role setting with limited privileges."}
            ])
            await conn.commit()

            stmt = select(Role.id).where(Role.name == 'Admin')
            data = await conn.execute(stmt)
            challenge = str(os.getenv('API_ADMIN_PASSWORD', 'admin'))
            hashed = await make_hash(challenge)
            await conn.execute(insert(User), [
                {"fname": "Fairuz", "lname": "Tahir", "email": os.getenv(
                    'API_ADMIN_EMAIL', 'admin@gmail.com'), "challenge": hashed, "role_id": data.scalar()}
            ])
            await conn.commit()
        await conn.close()


async def drop_db(app):
    async with app.db.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


def add_middleware(app):
    app.config.SECRET = os.getenv('JWT_SECRET', 'secret')
    _base_model_session_ctx = ContextVar("session")

    @app.middleware("request")
    async def inject_session(request):
        request.ctx.session = sessionmaker(
            app.db, AsyncSession, expire_on_commit=False)()
        request.ctx.session_ctx_token = _base_model_session_ctx.set(
            request.ctx.session)

    @app.middleware("response")
    async def close_session(request, response):
        if hasattr(request.ctx, "session_ctx_token"):
            _base_model_session_ctx.reset(request.ctx.session_ctx_token)
            await request.ctx.session.close()
