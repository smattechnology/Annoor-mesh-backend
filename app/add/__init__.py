from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.products.models import Product
from app.database import get_db

router = APIRouter(prefix="/add")

@router.post("/menu")
async def add_menu():
    pass