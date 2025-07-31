import uuid
from datetime import timedelta
from fastapi import APIRouter, Response, Request, Depends, HTTPException, status

from app.auth.models import User, Email, RoleEnum, Password, Info, StatusEnum
from app.database import get_db
from sqlalchemy.orm import Session
from app.utils import create_access_token, verify_access_token, generate_username, NameParser

from app.auth.schemas import UserLogin, UserRegister, UserResponse

router = APIRouter()


@router.get("/")
async def get_auth(request: Request, db: Session = Depends(get_db)):
    # 1. Get token from cookie
    access_token = request.cookies.get("access_token")
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
            detail="Client not found"
        )

    # 4. Success
    return {
        "client": user.as_dict(),
    }


@router.post("/login")
async def get_login(data: UserLogin, response: Response, db: Session = Depends(get_db)):
    if not all([data.username_or_email, data.password]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="All fields are required."
        )

    user: User = db.query(User).filter(User.username == data.username_or_email).first()
    if not user:
        by_email = db.query(Email).filter(Email.email == data.username_or_email).first()
        if not by_email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        user = db.query(User).filter(User.id == by_email.user_id).first()
    # If not found or password is incorrect
    if not user or not user.active_password().password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

        # (Optional) You can generate and return a JWT token here
        # Create JWT token
    token_data = {"sub": str(user.id)}  # you can include more data if needed
    token = create_access_token(data=token_data, expires_delta=timedelta(minutes=60))

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="lax",
        domain="nuraloom.xyz"
    )

    return {
        "user_id": user.id,
        "client_name": user.info.name,
        "token": token
    }


@router.post("/register")
async def get_register(data: UserRegister, response: Response, db: Session = Depends(get_db)):
    if not all([data.name, data.email, data.password]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="All fields (username, name, password) are required."
        )

    # Check if username or email already exists
    existing_email = db.query(Email).filter(Email.email == data.email).first()

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists."
        )

    uid = str(uuid.uuid4())

    new_user = User(
        id=uid,
        username=data.username if data.username else generate_username(data.email),
        role=data.role if data.role else RoleEnum.USER
    )

    new_email = Email(
        user_id=uid,
        email=data.email
    )

    new_password = Password(
        user_id=uid,
        password=data.password
    )
    name_parser = NameParser(data.name)
    new_info = Info(
        user_id=uid,
        name=name_parser.get_full_name(),
        firstMame=name_parser.get_first_name(),
        middleName=name_parser.get_middle_name(),
        lastName=name_parser.get_last_name()
    )

    db.add(new_user)
    db.add(new_email)
    db.add(new_password)
    db.add(new_info)
    db.commit()
    db.refresh(new_user)

    # Create JWT token
    token_data = {"sub": str(new_user.id)}  # you can include more data if needed
    token = create_access_token(data=token_data, expires_delta=timedelta(minutes=60))

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="lax",
        domain="annoor.nuraloom.xyz"
    )
    return {
        "user_id": new_user.id,
        "client_name": new_user.info.name,
        "token": token
    }


@router.get("/logout")
async def get_logout(response: Response, request: Request):
    access_token = request.cookies.get("access_token")

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token missing in cookies"
        )

    payload = verify_access_token(access_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="lax",
        domain="nuraloom.xyz"
    )

    return {
        "message": "Successfully logged out."
    }


