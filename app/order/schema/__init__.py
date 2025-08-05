from pydantic import BaseModel
from typing import List, Optional


class MealTime(BaseModel):
    breakfast: Optional[bool] = False
    lunch: Optional[bool] = False
    dinner: Optional[bool] = False


class OrderItem(BaseModel):
    product_id: str
    price: int  # or float, depending on your frontend
    bld: MealTime


class OrderPlaceSchema(BaseModel):
    mess_id: str
    meal_budget: int
    total_meal: int
    items: List[OrderItem]
