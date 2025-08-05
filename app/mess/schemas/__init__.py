from pydantic import BaseModel
from typing import Optional

from app.mess.models import MessTypeEnum


class OwnerSchema(BaseModel):
    name: str
    phone: str


class AddressSchema(BaseModel):
    street: str
    area: str
    city: str
    postalCode: int


class MessSchema(BaseModel):
    name: str
    type: MessTypeEnum
    phone: str
    owner: OwnerSchema
    address: AddressSchema
