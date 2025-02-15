from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper
from core.schemas import UserRead, TokenSchema
from auth.utils import create_access_token, create_refresh_token, create_verification_token
from auth.validations import validate_create_user, validate_auth_user
from auth.dependencies import (
    get_user_from_refresh_token,
    http_bearer,
    get_user_from_token_sub,
    get_token_payload,
)
from crud.users import UserDAO
from services.email import send_email

auth_router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=["Auth"],
    dependencies=[Depends(http_bearer)],
)


@auth_router.post("/register")
async def register(user: UserRead = Depends(validate_create_user)):
    verification_token = create_verification_token(user=user)
    await send_email(
        to_email=user.email,
        subject="Email Verification",
        body=f"Click the link to verify your email: {settings.api.v1.auth}/verify?token={verification_token}",
    )
    return {"message": "Registration completed successfully. Confirm your email address."}


@auth_router.post("/login", response_model=TokenSchema)
async def login(user: UserRead = Depends(validate_auth_user)):
    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)
    return TokenSchema(access_token=access_token, refresh_token=refresh_token)


@auth_router.post("/verify", response_model=UserRead)
async def verify_user(
    token: str,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    payload = await get_token_payload(token=token)
    user = await get_user_from_token_sub(payload=payload, token_type="access", session=session)

    if not user.is_verified:
        await UserDAO.verify_user(user_id=user.id, session=session)

        return user

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="User is already verified.",
    )


@auth_router.post(
    "/refresh",
    response_model=TokenSchema,
    response_model_exclude_none=True,
)
async def refresh_jwt(user: UserRead = Depends(get_user_from_refresh_token)):
    access_token = create_access_token(user=user)
    return TokenSchema(access_token=access_token)
