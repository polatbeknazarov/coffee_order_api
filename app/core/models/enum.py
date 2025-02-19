import enum


class UserRole(str, enum.Enum):
    USER: str = "user"
    ADMIN: str = "admin"


class OrderStatus(str, enum.Enum):
    PENDING: str = "pending"
    PROCESSING: str = "processing"
    COMPLETED: str = "completed"
    CANCELLED: str = "cancelled"
