import re
from pydantic import BaseModel, EmailStr, field_validator, ValidationInfo


class LoginRequest(BaseModel):
    username_or_email: str
    password: str


class RegisterRequest(BaseModel):
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
        pattern = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[!@#$%^&*()_]).{8,}$"

        if not re.match(pattern, password_value):
            raise ValueError("Password must be at least 8 characters long, contain at least one letter and one number.")

        return password_value


class VerifyRequest(BaseModel):
    token: str


class VerificationUserData(BaseModel):
    is_verified: bool = True
