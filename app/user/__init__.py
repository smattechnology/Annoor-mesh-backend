from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, desc, asc, and_, func

from app.auth import StatusEnum
from app.auth.models import User, Info, Email
from app.database import get_db

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
