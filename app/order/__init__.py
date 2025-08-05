import uuid
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session

from app.auth.models import User
from app.database import get_db
from app.dependencies import Admin
from app.order.models import Order, OrderItem
from app.order.schema import OrderPlaceSchema
from app.products.models import Product

add = APIRouter(prefix="/add")


@add.post("/",status_code=201)
async def place_order(data: OrderPlaceSchema, user: User = Depends(Admin), db: Session = Depends(get_db)):
    order_id = str(uuid.uuid4())
    new_order = Order(
        id=order_id,
        order_for=data.mess_id,
        order_by=user.id,
        meal_budget=data.meal_budget,
        total_meal=data.total_meal,
    )
    db.add(new_order)
    for item in data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            continue
        order_item_id = str(uuid.uuid4())
        new_order_item = OrderItem(
            id=order_item_id,
            order_id=order_id,
            product_id=product.id,
            current_price=product.price,
            price=item.price,
            for_breakfast=item.bld.breakfast,
            for_lunch=item.bld.lunch,
            for_dinner=item.bld.dinner
        )
        db.add(new_order_item)

    db.commit()
    db.refresh(new_order)


    return new_order.as_dict()
