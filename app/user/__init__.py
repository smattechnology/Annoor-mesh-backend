from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Depends, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, desc, asc, and_, func

from app.auth import StatusEnum
from app.auth.models import User, Info, Email
from app.database import get_db
from app.dependencies import Admin
from app.mess import Mess
from app.user.schemas import UpdateUserSchema
from app.utils import NameParser

router = APIRouter()


@router.get("/all")
async def get_users(
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
    query = db.query(User).join(User.info).outerjoin(User.emails).options(joinedload(User.info))

    # Filters
    if role:
        query = query.filter(User.role == role)
    if status:
        query = query.filter(User.status == status)

    if search:
        query = query.filter(
            and_(
                or_(
                    User.id.ilike(f"%{search}%"),
                    User.username.ilike(f"%{search}%"),
                    Info.name.ilike(f"%{search}%"),
                    Email.email.ilike(f"%{search}%"),
                ),
                Email.status == StatusEnum.ACTIVE
            )
        )

    # Sorting
    if sort_by == "name":
        sort_column = Info.name
    elif hasattr(User, sort_by):
        sort_column = getattr(User, sort_by)
    else:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by field: {sort_by}")

    query = query.order_by(desc(sort_column) if sort_order == "desc" else asc(sort_column))

    total = query.distinct(User.id).count()

    users = query.distinct(User.id).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "users": [user.as_dict() for user in users]
    }


@router.post("/update")
async def update_user(
        data: UpdateUserSchema,
        admin: User = Depends(Admin),
        db: Session = Depends(get_db)
):
    try:
        if not data.id:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="User ID not present in payload"
            )

        user: User = db.query(User).filter(User.id == data.id).first()
        if not user:মাংস (Meat)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        if not user.info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User info not found"
            )

        if data.name:
            name_parser = NameParser(data.name)
            user.info.name = name_parser.get_full_name()
            user.info.firstName = name_parser.get_first_name()
            user.info.middleName = name_parser.get_middle_name()
            user.info.lastName = name_parser.get_last_name()

        if data.email:
            active_email = user.active_email()
            if active_email:
                active_email.status = StatusEnum.DISABLED
            new_email = Email(
                user_id=user.id,
                email=data.email
            )
            db.add(new_email)

        if data.dob:
            user.info.dob = data.dob

        if data.address:
            user.info.address = data.address

        if data.role:
            user.role = data.role

        if data.status:
            user.status = data.status

        db.commit()
        db.refresh(user)

        return user.as_dict()

    except SQLAlchemyError as db_err:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error occurred: {str(db_err)}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )


@router.post("/update/mess")
async def update_mess(user_id: str, mess_id: str, admin: User = Depends(Admin),
                      db: Session = Depends(get_db)):

    if not user_id and not mess_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User ID and Mess ID are's not present in payload"
        )

    user:User = db.query(User).filter(User.id == user_id).first()

    mess = db.query(Mess).filter(Mess.id == mess_id).first()

    if not user and not mess:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User and Mess are's not present in server"
        )

    user.allocated_mess_id = mess_id

    db.commit()
    db.refresh(user)

    return user.as_dict()