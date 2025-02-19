__all__ = (
    "send_welcome_email",
    "send_email_verification_token",
)

import logging
import sys

from core.config import settings
from .email_notification import (
    send_welcome_email,
    send_email_verification_token,
)

if sys.argv[0] == "worker":
    logging.basicConfig(
        level=settings.logging.log_level_value,
        format=settings.logging.log_format,
    )
