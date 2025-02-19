import logging

from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import User, UserRole
from core.schemas import UserAdminCreate
from crud.users import UserDAO
from auth.utils import hash_password

log = logging.getLogger(__name__)


async def create_admin(
    session: AsyncSession,
    username: str = settings.admin.username,
    email: str = settings.admin.email,
    password: str = settings.admin.password,
):
    admin_exists = await UserDAO.get_user_by_email_or_username(
        username=username,
        email=email,
        session=session,
    )
    if admin_exists:
        log.info("Admin user already exists.")
        return

    hashed_password = hash_password(password=password)
    admin_data = UserAdminCreate(
        username=username,
        email=email,
        hashed_password=hashed_password,
        role=UserRole.ADMIN,
    )

    new_admin_user = await UserDAO.create(validated_values=admin_data, session=session)
    return new_admin_user
