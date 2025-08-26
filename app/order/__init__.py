from uuid import uuid4
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session, joinedload

from app.auth.models import User
from app.database import get_db
from app.dependencies import Admin
from app.mess import Mess
from app.order.models import Order, OrderItem, NoteOrder, NoteOrderItem, MealTimeEnum
from app.order.schema import OrderPlaceSchema, NoteOrderInfo, NoteOrderPlaceSchema
from app.products.models import Product

add = APIRouter(prefix="/add")
get = APIRouter(prefix="/get")


@add.post("/", status_code=201)
async def place_order(
        data: OrderPlaceSchema,
        user: User = Depends(Admin),
        db: Session = Depends(get_db)
):
    try:
        order_id = str(uuid4())
        new_order = Order(
            id=order_id,
            order_for=data.mess_id,
            order_by=user.id,
            meal_budget=data.budgetPerMeal,
            total_meal=data.totalMeal,
        )
        db.add(new_order)

        for item in data.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if not product:
                continue

            order_item_id = str(uuid4())
            new_order_item = OrderItem(
                id=order_item_id,
                order_id=order_id,
                product_id=product.id,
                unit_id=item.unit_id,
                auto=item.auto,
                quantity=item.quantity,
                for_breakfast=getattr(item.bld, "breakfast", False),
                for_lunch=getattr(item.bld, "lunch", False),
                for_dinner=getattr(item.bld, "dinner", False)
            )
            db.add(new_order_item)

        db.commit()
        db.refresh(new_order)
        return new_order.as_dict()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@get.get("/all")
async def get_orders(
        search: Optional[str] = Query(None, description="Search term for username, name or email"),
        limit: int = Query(10, gt=0, le=100, description="Number of items per page"),
        skip: int = Query(0, ge=0, description="Number of items to skip"),
        sort_by: Optional[str] = Query("created_at", description="Field to sort by"),
        sort_order: Optional[str] = Query("desc", description="Sort order (asc/desc)"),
        role: Optional[str] = Query(None, description="Filter by role"),
        status: Optional[str] = Query(None, description="Filter by status"),
        db: Session = Depends(get_db)
):
    # Base query with joins
    query = db.query(Order).options(
        joinedload(Order.user),  # eager load user
        joinedload(Order.mess),  # eager load mess
        joinedload(Order.items),  # eager load items
    )
    # Filters
    if role:
        query = query.filter(User.role == role)
    if status:
        query = query.filter(User.status == status)

    # Search by user name, email, or mess name
    if search:
        query = query.join(User).join(Mess).filter(
            or_(
                User.name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%"),
                Mess.name.ilike(f"%{search}%"),
                Order.id.ilike(f"%{search}%"),
            )
        )

    total = query.distinct(User.id).count()

    orders = query.distinct(User.id).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "orders": [order.as_dict() for order in orders]
    }

@add.post("/note_order",status_code=201)
async def add_note_order(
        data: NoteOrderPlaceSchema,
        user: User = Depends(Admin),
        db: Session = Depends(get_db)
):
    # Validate user

    if not user.allocated_mess_id:
        raise HTTPException(status_code=400, detail="User has no allocated mess")

    # Validate meal data
    if not (data.breakfast or data.lunch or data.dinner):
        raise HTTPException(status_code=400, detail="At least one meal is required")

    order_id = str(uuid4())

    # Create NoteOrder
    new_order = NoteOrder(
        id=order_id,
        order_for=user.allocated_mess_id,
        order_by=user.id
    )
    db.add(new_order)

    # Prepare meals in a dictionary for easy loop
    meals_map = {
        MealTimeEnum.BREAKFAST: data.breakfast,
        MealTimeEnum.LUNCH: data.lunch,
        MealTimeEnum.DINNER: data.dinner
    }

    for meal_time, meal_data in meals_map.items():
        if meal_data:
            new_order_item = NoteOrderItem(
                id=str(uuid4()),
                order_id=order_id,
                meal_time=meal_time,
                meal_budget=meal_data.budget,
                total_meal=meal_data.students,
                note=meal_data.note
            )
            db.add(new_order_item)

    db.commit()
    db.refresh(new_order)

    return new_order.as_dict()

    # @add.post("/update-status")
    # async def update_status(data: OrderPlaceSchema,
    #         user: User = Depends(Admin),
    #         db: Session = Depends(get_db))


@get.get("/note/all")
async def get_note_orders(
        search: Optional[str] = Query(None, description="Search term for username, name or email"),
        limit: int = Query(10, gt=0, le=100, description="Number of items per page"),
        skip: int = Query(0, ge=0, description="Number of items to skip"),
        sort_by: Optional[str] = Query("created_at", description="Field to sort by"),
        sort_order: Optional[str] = Query("desc", description="Sort order (asc/desc)"),
        role: Optional[str] = Query(None, description="Filter by role"),
        status: Optional[str] = Query(None, description="Filter by status"),
        db: Session = Depends(get_db)
):
    # Base query with joins
    query = db.query(NoteOrder).options(
        joinedload(NoteOrder.user),  # eager load user
        joinedload(NoteOrder.mess),  # eager load mess
        joinedload(NoteOrder.items),  # eager load items
    )
    # Filters
    if role:
        query = query.filter(User.role == role)
    if status:
        query = query.filter(User.status == status)

    # Search by user name, email, or mess name
    if search:
        query = query.join(User).join(Mess).filter(
            or_(
                User.name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%"),
                Mess.name.ilike(f"%{search}%"),
                NoteOrder.id.ilike(f"%{search}%"),
            )
        )

    total = query.distinct(User.id).count()

    orders = query.distinct(User.id).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "orders": [order.as_dict() for order in orders]
    }