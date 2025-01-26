import bcrypt
import jwt

from datetime import datetime, timezone, timedelta

from core.config import settings
from core.schemas import UserRead


def encode_jwt(
    payload: dict,
    expire_minutes: int,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
) -> str:
    to_encode = payload.copy()

    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(exp=expire, iat=now)
    encoded = jwt.encode(payload=to_encode, key=private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    decoded = jwt.decode(jwt=token, key=public_key, algorithms=[algorithm])

    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    password_bytes: bytes = password.encode()
    return bcrypt.hashpw(password_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int,
) -> str:
    payload = {"type": token_type}
    payload.update(token_data)
    return encode_jwt(payload=payload, expire_minutes=expire_minutes)


def create_access_token(user: UserRead) -> str:
    payload = {"sub": str(user.id), "username": user.username, "email": user.email}
    return create_jwt(
        token_type="access",
        token_data=payload,
        expire_minutes=settings.auth_jwt.access_token_expire_minutes,
    )


def create_refresh_token(user: UserRead) -> str:
    payload = {"sub": str(user.id)}
    return create_jwt(
        token_type="refresh",
        token_data=payload,
        expire_minutes=settings.auth_jwt.refresh_token_expire_minutes,
    )
