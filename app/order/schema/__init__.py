from pydantic import BaseModel, Field
from typing import List, Optional


class MealTime(BaseModel):
    breakfast: bool = Field(default=False)
    lunch: bool = Field(default=False)
    dinner: bool = Field(default=False)


class OrderItem(BaseModel):
    product_id: str
    auto: bool
    quantity: int = Field(ge=0)  # Non-negative quantity
    bld: MealTime
    unit_id: Optional[str] = None


class OrderPlaceSchema(BaseModel):
    user_id: str
    mess_id: str
    totalMeal: int = Field(gt=0)  # Must be greater than 0
    budgetPerMeal: int = Field(gt=0)  # Must be greater than 0
    items: List[OrderItem]


class NoteOrderInfo(BaseModel):
    budget: int
    students: int
    note: str

class NoteOrderPlaceSchema(BaseModel):
    breakfast: Optional[NoteOrderInfo] = None
    lunch: Optional[NoteOrderInfo] = None
    dinner: Optional[NoteOrderInfo] = None
