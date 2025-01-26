from fastapi import APIRouter, Depends

from core.config import settings
from core.schemas import UserRead, TokenSchema
from auth.utils import create_access_token, create_refresh_token
from auth.validations import validate_create_user, validate_auth_user
from auth.dependencies import get_user_from_refresh_token, http_bearer

auth_router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=["Auth"],
    dependencies=[Depends(http_bearer)],
)


@auth_router.post("/register", response_model=UserRead)
async def register(user: UserRead = Depends(validate_create_user)):
    return user


@auth_router.post("/login", response_model=TokenSchema)
async def login(user: UserRead = Depends(validate_auth_user)):
    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)
    return TokenSchema(access_token=access_token, refresh_token=refresh_token)
