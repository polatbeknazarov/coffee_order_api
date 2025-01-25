import re
from pydantic import BaseModel, EmailStr, field_validator, ValidationInfo


class LoginRequest(BaseModel):
    username_or_email: str
    password: str


class RegisterRequest(LoginRequest):
    username: str
    email: EmailStr
    password: str
    confirm_password: str

    @field_validator("confirm_password")
    def passwords_match(cls, v: str, info: ValidationInfo):
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Password does not match.")
        return v

    @field_validator("password")
    def password_validation(cls, password_value: str):
        password_value = password_value.strip()

        if len(password_value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", password_value):
            raise ValueError("The password must contain at least one capital letter.")
        if not re.search(r"[0-9]", password_value):
            raise ValueError("The password must contain at least one number.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password_value):
            raise ValueError("The password must contain at least one special character.")

        return password_value
