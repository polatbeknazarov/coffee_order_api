import logging

from datetime import datetime, timedelta

from core.config import settings
from core.models import db_helper
from crud.users import UserDAO

log = logging.getLogger(__name__)


async def remove_unverified_users():
    async with db_helper.session_factory() as session:
        expiration_time = datetime.utcnow() - timedelta(
            minutes=settings.auth_jwt.verification_token_expire_minutes,
        )
        unverified_users = await UserDAO.find_all(
            where={"is_verified": False},
            session=session,
        )

        for user in unverified_users:
            if user.created_at < expiration_time:
                await UserDAO.delete(model_id=user.id, session=session)
                log.info(f"Deleted unverified user {user.id}")

        if not unverified_users:
            log.info("No unverified users to delete")
