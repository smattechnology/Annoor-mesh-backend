from typing import Optional

from pydantic import BaseModel


class CategorySchema(BaseModel):
    label: str
    icon: Optional[str] = None


class UniteSchema(BaseModel):
    label: str
    icon: Optional[str] = None


class ProductSchema(BaseModel):
    name: str
    price: int
    unite_id: str
    category_id: str
    description: Optional[str] = None
