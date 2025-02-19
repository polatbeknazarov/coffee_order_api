from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from core.config import settings
from core.models import db_helper, UserRole
from core.schemas import (
    StaticInfoRead,
    StaticInfoCreate,
    StaticInfoUpdate,
    UserRead,
)
from auth.dependencies import http_bearer, require_role
from crud.static_info import StaticInfoDAO

static_info_router = APIRouter(
    prefix=settings.api.v1.static_info,
    tags=["Static Info"],
    dependencies=[Depends(http_bearer)],
)


@static_info_router.post("", response_model=StaticInfoRead)
async def create_static_info(
    request: StaticInfoCreate,
    admin: UserRead = Depends(require_role(UserRole.ADMIN)),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        static_info = await StaticInfoDAO.create(
            validated_values=request,
            session=session,
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Static info with key "{request.key}" already exists.',
        )

    return static_info


@static_info_router.get("", response_model=List[StaticInfoRead])
async def get_all_static_info(
    admin: UserRead = Depends(require_role(UserRole.ADMIN)),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    static_info = await StaticInfoDAO.get_all(session=session)
    return static_info


@static_info_router.patch("/{static_info_id}", response_model=StaticInfoRead)
async def update_static_info_by_id(
    static_info_id: int,
    request: StaticInfoUpdate,
    admin: UserRead = Depends(require_role(UserRole.ADMIN)),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    result = await StaticInfoDAO.update(
        model_id=static_info_id,
        validated_values=request,
        session=session,
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Static info with id "{static_info_id}" not found.',
        )

    return result


@static_info_router.delete("/{static_info_id}")
async def delete_static_info_by_id(
    static_info_id: int,
    admin: UserRead = Depends(require_role(UserRole.ADMIN)),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    result = await StaticInfoDAO.delete(
        model_id=static_info_id,
        session=session,
    )
    return result
