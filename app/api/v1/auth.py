from fastapi import APIRouter

from core.config import settings

auth_router = APIRouter(prefix=settings.api.v1.auth, tags=["Auth"])
