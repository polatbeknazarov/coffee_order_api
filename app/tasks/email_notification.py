import logging

from core.taskiq_broker import broker
from core.config import settings
from services.mailing import send_email, send_welcome_email as send


log = logging.getLogger(__name__)


@broker.task
async def send_welcome_email(user_email: str, username: str) -> None:
    log.info("Sending welcome email to user with email: %s", user_email)
    await send(user_email=user_email, username=username)


@broker.task
async def send_email_verification_token(
    user_email: str,
    verification_token: str,
) -> None:
    log.info("Sending verification token to user with email: %s", user_email)
    await send_email(
        to_email=user_email,
        subject="Email Verification",
        body=(
            f"Click the link to verify your email: http://localhost:8000{settings.api.v1.auth}/verify?token={verification_token}"
        ),
    )
