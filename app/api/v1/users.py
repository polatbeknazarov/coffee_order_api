from fastapi import APIRouter, Depends

from core.config import settings
from core.schemas import UserRead
from auth.dependencies import get_current_user, http_bearer

users_router = APIRouter(
    prefix=settings.api.v1.users,
    tags=["Users"],
    dependencies=[Depends(http_bearer)],
)


@users_router.get("/me", response_model=UserRead)
async def get_current_auth_user(
    user: UserRead = Depends(get_current_user),
):
    return user
