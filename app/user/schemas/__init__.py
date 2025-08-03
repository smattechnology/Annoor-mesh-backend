from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from enum import Enum
from datetime import date

from app.auth import RoleEnum
from app.auth.models import StatusEnum


class UpdateUserSchema(BaseModel):
    id:str
    email: Optional[EmailStr] = None
    role: Optional[RoleEnum] = None
    status: Optional[StatusEnum] = None
    name: Optional[str] = None
    dob: Optional[str] = None
    address: Optional[str] = None

    class Config:
        orm_mode = True
