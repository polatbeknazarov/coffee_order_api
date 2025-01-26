from fastapi import APIRouter, Depends

from core.config import settings
from core.schemas import UserRead, TokenSchema
from auth.utils import encode_jwt
from auth.validations import validate_create_user, validate_auth_user

auth_router = APIRouter(prefix=settings.api.v1.auth, tags=["Auth"])


@auth_router.post("/register", response_model=UserRead)
async def register(user: UserRead = Depends(validate_create_user)):
    return user


@auth_router.post("/login", response_model=TokenSchema)
async def login(user: UserRead = Depends(validate_auth_user)):
    payload = {"sub": str(user.id), "username": user.username, "email": user.email}
    access_token = encode_jwt(payload=payload)
    return TokenSchema(access_token=access_token, token_type="Bearer")
