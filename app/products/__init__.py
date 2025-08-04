import uuid
from time import sleep
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, Query, joinedload

from app.auth import User
from app.database import get_db
from app.dependencies import Admin
from app.products.models import Category, Unite, Product
from app.products.schemas import CategorySchema, UniteSchema, ProductSchema

add = APIRouter(prefix="/add")
get = APIRouter(prefix="/get")


@add.post("/category", status_code=status.HTTP_201_CREATED)
async def add_category(
        data: CategorySchema,
        admin: User = Depends(Admin),
        db: Session = Depends(get_db)
):
    # Check if category already exists
    existing_category = db.query(Category).filter_by(label=data.label).first()
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with value '{data.label}' already exists."
        )

    # Attempt to create and save new category
    try:
        new_category = Category(
            id=str(uuid.uuid4()),
            label=data.label,
            icon=data.icon
        )
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category.as_dict()

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal error occurred while creating the category."
        )


@add.post("/unite", status_code=status.HTTP_201_CREATED)
async def add_unite(
        data: UniteSchema,
        admin: User = Depends(Admin),
        db: Session = Depends(get_db)
):
    # Check if unite already exists
    existing_unite = db.query(Unite).filter_by(label=data.label).first()
    if existing_unite:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unite with value '{data.label}' already exists."
        )

    try:
        new_unite = Unite(
            id=str(uuid.uuid4()),
            label=data.label,
            icon=data.icon
        )
        db.add(new_unite)
        db.commit()
        db.refresh(new_unite)
        return new_unite.as_dict()

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal error occurred while creating the unite."
        )


@get.get("/category/all")
async def get_all_category(admin: User = Depends(Admin),
                           db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return [category.as_dict() for category in categories]


@get.get("/unite/all")
async def get_all_unite(admin: User = Depends(Admin),
                        db: Session = Depends(get_db)):
    unites = db.query(Unite).all()
    return [unite.as_dict() for unite in unites]


@add.post("/", status_code=201)
async def add_product(data: ProductSchema, admin: User = Depends(Admin), db: Session = Depends(get_db)):
    existing_product = db.query(Product).filter(Product.name == data.name, Product.unite_id == data.category_id,
                                                Product.unite_id == data.unite_id).first()

    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product '{data.name}' already exists."
        )

    new_product = Product(
        id=str(uuid4()),
        name=data.name,
        price=data.price,
        description=(data.description if data.description else None),
        category_id=data.category_id,
        unite_id=data.unite_id
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product.as_dict()


# @get.get("/all")
# async def get_all_product(admin: User = Depends(Admin),
#                           search: Optional[str] = Query(None, description="Search term for username, name or email"),
#                           limit: int = Query(10, gt=0, le=100, description="Number of items per page"),
#                           skip: int = Query(0, ge=0, description="Number of items to skip"),
#                           sort_by: Optional[str] = Query("created_at", description="Field to sort by"),
#                           sort_order: Optional[str] = Query("desc", description="Sort order (asc/desc)"),
#                           role: Optional[str] = Query(None, description="Filter by role"),
#                           status: Optional[str] = Query(None, description="Filter by status"),
#                           db: Session = Depends(get_db)
#                           ):
#     query = db.query(Product).join(Product.category).outerjoin(Product.unite).options(joinedload(Product.category))
