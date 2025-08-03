from typing import Optional

from pydantic import BaseModel


class CategorySchema(BaseModel):
    value: str
    label: str
    icon: Optional[str] = None

class UniteSchema(BaseModel):
    value: str
    label: str
    icon: Optional[str] = None

class ProductSchema(BaseModel):
    name:str
    price:str
    unite_id:str
    category_id:str
    description:Optional[str] = None