from typing import Optional

from pydantic import BaseModel, EmailStr

from app.auth import RoleEnum


class User(BaseModel):
    email: EmailStr
    username: Optional[str] = None


class UserRegister(User):
    name: str
    password: str
    role: RoleEnum or None = None


class UserResponse(User):
    name: str
    token: str


class UserLogin(BaseModel):
    username_or_email: str
    password: str
