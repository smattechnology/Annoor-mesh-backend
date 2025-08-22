from typing import Optional, List

from pydantic import BaseModel, Field


class CategorySchema(BaseModel):
    label: str
    icon: Optional[str] = None


class UniteSchema(BaseModel):
    label: str
    icon: Optional[str] = None


# Schemas
class ItemUnite(BaseModel):
    unit_id: str
    price: int = Field(gt=0)
    is_generic: bool = False

class ProductSchema(BaseModel):
    name: str
    category_id: str
    units: List[ItemUnite]
    description: Optional[str] = None

