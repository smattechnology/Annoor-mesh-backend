import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.mess.models import Mess
from app.database import get_db
from app.mess.schemas import MessSchema
from sqlalchemy import or_, desc, asc

router = APIRouter()


@router.post("/add")
async def add_mess(data: MessSchema, db: Session = Depends(get_db)):
    if not all([data.name, data.address]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="All fields (Name, Address) are required."
        )

    existing_mess = db.query(Mess).filter(
        Mess.name == data.name,
        Mess.address == data.address
    ).first()

    if existing_mess:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mess already exists."
        )

    new_mess = Mess(
        id=str(uuid.uuid4()),
        name=data.name,
        address=data.address,
        phone=data.phone or None
    )

    db.add(new_mess)
    db.commit()
    db.refresh(new_mess)

    return {"status": "Successfully added"}


@router.get("/all")
async def get_users(
    search: Optional[str] = Query(None, description="Search term for name, address or phone"),
    limit: int = Query(10, gt=0, le=100),
    skip: int = Query(0, ge=0),
    sort_by: Optional[str] = Query("created_at"),
    sort_order: Optional[str] = Query("desc"),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Mess)

    if status:
        query = query.filter(Mess.status == status)

    if search:
        query = query.filter(
            or_(
                Mess.id.ilike(f"%{search}%"),
                Mess.name.ilike(f"%{search}%"),
                Mess.address.ilike(f"%{search}%"),
                Mess.phone.ilike(f"%{search}%"),
            )
        )

    try:
        sort_column = getattr(Mess, sort_by)
    except AttributeError:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by field: {sort_by}")

    query = query.order_by(desc(sort_column) if sort_order == "desc" else asc(sort_column))

    total = query.distinct(Mess.id).count()
    messes = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "messes": [mess.as_dict() for mess in messes]
    }
