import logging
import uvicorn

from core.config import settings
from create_fastapi_app import create_app

from api import router as api_router

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
    format="[%(asctime)s.%(msecs)03d] %(module)20s:%(lineno)-3d %(levelname)-7s - %(message)s",
)


main_app = create_app()
main_app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
