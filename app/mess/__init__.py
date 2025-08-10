import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.mess.models import Mess, MessAddress, MessOwner, StatusEnum
from app.database import get_db
from app.mess.schemas import MessSchema
from sqlalchemy import or_, desc, asc, and_

router = APIRouter()


@router.post("/add", status_code=201)
async def add_mess(data: MessSchema, db: Session = Depends(get_db)):
    if not all([data.name, data.address]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="All fields (Name, Address) are required."
        )

    # Check if mess with same name and address exists
    existing_mess = db.query(Mess).join(MessAddress).filter(
        Mess.name == data.name,
        MessAddress.street == data.address.street,
        MessAddress.area == data.address.area,
        MessAddress.city == data.address.city,
        MessAddress.postalCode == data.address.postalCode
    ).first()

    if existing_mess:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mess already exists at this address."
        )

    # Create new entries
    mess_id = str(uuid.uuid4())
    owner_id = str(uuid.uuid4())
    address_id = str(uuid.uuid4())

    new_owner = MessOwner(
        id=owner_id,
        name=data.owner.name,
        phone=data.owner.phone,
    )

    new_address = MessAddress(
        id=address_id,
        street=data.address.street,
        area=data.address.area,
        city=data.address.city,
        postalCode=data.address.postalCode,
    )

    new_mess = Mess(
        id=mess_id,
        name=data.name,
        phone=data.phone,
        address_id=address_id,
        owner_id=owner_id,
        type=data.type,
    )

    db.add(new_owner)
    db.add(new_address)
    db.add(new_mess)
    db.commit()
    db.refresh(new_mess)

    return {"status": "Successfully added", "data": new_mess.as_dict()}


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


@router.get("/search")
async def get_mess_search(q: Optional[str] = Query(None, description="Search term for name, address or phone"),
                          db: Session = Depends(get_db)):
    query = db.query(Mess)

    if q:
        query = query.filter(
            and_(
                or_(
                    Mess.id.ilike(f"%{q}%"),
                    Mess.name.ilike(f"%{q}%"),
                    Mess.phone.ilike(f"%{q}%"),
                ),
                Mess.status == StatusEnum.ACTIVE
            )
        )

    messes = query.all()

    return {
        "messes": [mess.as_dict() for mess in messes]
    }