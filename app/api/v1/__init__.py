from fastapi import APIRouter

from core.config import settings
from .auth import auth_router
from .users import users_router
from .categories import categories_router
from .products import products_router
from .carts import carts_router
from .orders import orders_router
from .static_info import static_info_router
from .chats import chats_router
from .messages import messages_router

api_v1_router = APIRouter(prefix=settings.api.v1.prefix)

api_v1_router.include_router(auth_router)
api_v1_router.include_router(users_router)
api_v1_router.include_router(categories_router)
api_v1_router.include_router(products_router)
api_v1_router.include_router(carts_router)
api_v1_router.include_router(orders_router)
api_v1_router.include_router(static_info_router)
api_v1_router.include_router(chats_router)
api_v1_router.include_router(messages_router)
