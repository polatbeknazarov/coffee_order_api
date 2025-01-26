import logging

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jwt.exceptions import InvalidTokenError

from core.config import settings
from core.models import db_helper
from core.schemas import UserRead
from auth.utils import decode_jwt
from crud.users import UserDAO

http_bearer = HTTPBearer(auto_error=False)
oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.api.prefix}{settings.api.v1.prefix}{settings.api.v1.auth}/login"
)


async def get_token_payload(token: str = Depends(oauth2_schema)) -> UserRead:
    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError as e:
        logging.error("Invalid token error: %s. Token: %s", e, token)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token error.",
        )

    return payload


async def get_current_auth_user(
    payload: dict = Depends(get_token_payload),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> UserRead:
    token_type = payload.get("type")
    if token_type != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type.",
        )

    user_id = payload.get("sub")
    user = await UserDAO.get_by_id(model_id=int(user_id), session=session)

    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token.",
    )


async def get_current_user(user: UserRead = Depends(get_current_auth_user)):
    if user.is_active:
        return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User inactive.",
    )
