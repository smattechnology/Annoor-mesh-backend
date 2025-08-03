from fastapi import APIRouter, Response, Request, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.settings import settings
from app.auth import User, RoleEnum
from app.database import get_db
from app.utils import verify_access_token


def Admin(request: Request, db: Session = Depends(get_db)):
    # 1. Get token from cookie
    access_token = request.cookies.get(settings.FRONTEND_ACCESS_COOKIE_KEY)
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token missing in cookies"
        )

    # 2. Verify token
    payload = verify_access_token(access_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    # 3. Get admin from DB
    uid = payload.get("sub")
    user = db.query(User).filter(User.id == uid).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user.role != RoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Admins only"
        )

    return user