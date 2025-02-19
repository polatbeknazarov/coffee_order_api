import logging

from typing import Literal

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jwt.exceptions import InvalidTokenError

from core.config import settings
from core.models import db_helper, UserRole
from core.schemas import UserRead
from crud.users import UserDAO
from .utils import decode_jwt
from .validations import validate_token_type

log = logging.getLogger(__name__)

http_bearer = HTTPBearer(auto_error=False)
oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.api.prefix}{settings.api.v1.prefix}{settings.api.v1.auth}/login"
)


async def get_token_payload(token: str = Depends(oauth2_schema)) -> dict:
    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError as e:
        log.error("Invalid token error: %s. Token: %s", e, token)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token error.",
        )

    return payload


async def get_user_from_token_sub(
    payload: dict,
    token_type: Literal["access", "refresh"],
    session: AsyncSession,
) -> UserRead:
    validate_token_type(payload=payload, token_type=token_type)

    user_id = payload.get("sub")
    user = await UserDAO.get_by_id(model_id=int(user_id), session=session)

    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token.",
    )


async def get_current_auth_user(
    payload: dict = Depends(get_token_payload),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> UserRead:
    return await get_user_from_token_sub(
        payload=payload,
        token_type="access",
        session=session,
    )


async def get_user_from_refresh_token(
    payload: dict = Depends(get_token_payload),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> UserRead:
    return await get_user_from_token_sub(
        payload=payload,
        token_type="refresh",
        session=session,
    )


async def get_current_user(user: UserRead = Depends(get_current_auth_user)):
    if user.is_active and user.is_verified:
        return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User inactive.",
    )


def require_role(required_role: UserRole):
    def role_checker(user: UserRead = Depends(get_current_user)) -> UserRead:
        if user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this resource.",
            )
        return user

    return role_checker


async def get_unverified_user_by_email(
    email: str, session: AsyncSession = Depends(db_helper.session_getter)
):
    user = await UserDAO.get_user_by_email(email=email, session=session)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already verified.",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User inactive.",
        )

    return user
