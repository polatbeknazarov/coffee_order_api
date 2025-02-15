from fastapi import Form, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, User
from core.schemas import RegisterRequest, UserCreate
from crud.users import UserDAO
from auth.utils import hash_password, validate_password


async def validate_create_user(
    register_request: RegisterRequest,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> User:
    existing_user = await UserDAO.get_user_by_email_or_username(
        username=register_request.username,
        email=register_request.email,
        session=session,
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with username '{register_request.username}' already exists.",
        )

    hashed_password = hash_password(password=register_request.password)
    new_user_data = UserCreate(
        username=register_request.username,
        email=register_request.email,
        hashed_password=hashed_password,
    )
    new_user = await UserDAO.create(validated_values=new_user_data, session=session)
    return new_user


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> User:
    user = await UserDAO.get_user_by_email_or_username(
        username=username,
        email=username,
        session=session,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )

    if not validate_password(password=password, hashed_password=user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )

    if not user.is_active or not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User inactive.",
        )

    return user


def validate_token_type(payload: dict, token_type: str) -> bool:
    if payload.get("type") == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token type.",
    )
