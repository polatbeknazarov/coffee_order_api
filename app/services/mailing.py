import logging
import aiosmtplib

from email.message import EmailMessage

from core.config import settings

log = logging.getLogger(__name__)


async def send_email(to_email: str, subject: str, body: str):
    msg = EmailMessage()
    msg["From"] = settings.smtp.user
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        await aiosmtplib.send(
            msg,
            hostname=settings.smtp.host,
            port=settings.smtp.port,
            username=settings.smtp.user,
            password=settings.smtp.password,
            start_tls=True,
        )
        log.info("Email successfully sent to %s", to_email)
    except Exception as e:
        log.error("Error sending email: %s", e)
        raise e


async def send_welcome_email(user_email: str, username: str) -> None:
    await send_email(
        to_email=user_email,
        subject="Welcome to our site!",
        body=f"Dear {username},\n\nWelcome to our site!",
    )
