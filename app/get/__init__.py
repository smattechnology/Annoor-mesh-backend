from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.products.models import Product
from app.database import get_db

router = APIRouter(prefix="/get")

@router.get("/menu")
async def get_menu():
    pass

