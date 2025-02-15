import logging
import aiosmtplib

from email.message import EmailMessage

from core.config import settings


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
        logging.info("Email successfully sent to %s", to_email)
    except Exception as e:
        logging.error("Error sending email: %s", e)
        raise e
