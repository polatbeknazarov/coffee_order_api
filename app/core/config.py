from pathlib import Path

from pydantic import BaseModel, PostgresDsn, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class APIV1Prefix(BaseModel):
    prefix: str = "/v1"
    auth: str = "/auth"
    users: str = "/users"


class APIPrefix(BaseModel):
    prefix: str = "/api"
    v1: APIV1Prefix = APIV1Prefix()


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_minutes: int = 60 * 24 * 30
    verification_token_expire_minutes: int = 20


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 30
    pool_size: int = 10


class SMTPConfig(BaseModel):
    host: str
    port: int
    user: EmailStr
    password: str


class AdminConfig(BaseModel):
    email: EmailStr
    username: str
    password: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )

    run: RunConfig = RunConfig()
    api: APIPrefix = APIPrefix()
    auth_jwt: AuthJWT = AuthJWT()
    db: DatabaseConfig
    smtp: SMTPConfig
    admin: AdminConfig


settings = Settings()
