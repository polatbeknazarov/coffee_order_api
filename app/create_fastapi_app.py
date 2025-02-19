from contextlib import asynccontextmanager
from fastapi import FastAPI

from core import broker
from core.models import db_helper
from core.scheduler import scheduler
from services.create_admin import create_admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.session_factory() as session:
        await create_admin(session=session)
    await broker.startup()
    scheduler.start()

    yield

    await broker.shutdown()
    scheduler.shutdown()
    await db_helper.dispose()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    return app
