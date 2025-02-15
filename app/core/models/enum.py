import enum


class UserRole(str, enum.Enum):
    USER: str = "user"
    ADMIN: str = "admin"
