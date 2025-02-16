from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.models import db_helper
from services.create_admin import create_admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.session_factory() as session:
        await create_admin(session=session)
    yield
    await db_helper.dispose()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    return app
