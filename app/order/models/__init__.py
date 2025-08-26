import enum
from pyexpat import native_encoding
from symtable import Class
from uuid import uuid4
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    DateTime,
    Integer,
    Boolean,
    Enum, false,
)
from sqlalchemy.orm import relationship
from app.database.base import Base


class OrderStatusEnum(enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"


class Order(Base):
    __tablename__ = "orders"

    id = Column(String(255), primary_key=True, default=lambda: str(uuid4()), index=True)

    order_for = Column(String(255), ForeignKey("messs.id", ondelete="CASCADE"), nullable=False)
    order_by = Column(String(255), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    meal_budget = Column(Integer, nullable=False)
    total_meal = Column(Integer, nullable=False)

    status = Column(
        Enum(OrderStatusEnum, native_enum=False), default=OrderStatusEnum.PENDING, nullable=False
    )

    items = relationship(
        "OrderItem", backref="order", cascade="all, delete-orphan", lazy="joined"
    )

    mess = relationship("Mess", backref="orders")  # Assuming Mess model exists
    user = relationship("User", backref="orders")  # Assuming User model exists

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def as_dict(self):
        return {
            "id": self.id,
            "user": self.user.as_dict() if self.user else None,
            "mess": self.mess.as_dict() if self.mess else None,
            "meal_budget": self.meal_budget,
            "total_meal": self.total_meal,
            "status": self.status.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "items": [item.as_dict() for item in self.items],
        }

    def __repr__(self):
        return f"<Order(id={self.id}, status={self.status}, meal_budget={self.meal_budget})>"


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(String(255), primary_key=True, default=lambda: str(uuid4()), index=True)

    order_id = Column(String(255), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(String(255), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    unit_id = Column(String(255), ForeignKey("items_unit.id", ondelete="CASCADE"), nullable=False)

    auto = Column(Boolean, default=True, nullable=False)
    quantity = Column(Integer, default=0, nullable=False)

    for_breakfast = Column(Boolean, nullable=False, default=False)
    for_lunch = Column(Boolean, nullable=False, default=False)
    for_dinner = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    product = relationship("Product", backref="order_items")
    unit = relationship("ItemUnit", backref="order_items")

    def as_dict(self):
        return {
            "id": self.id,
            "product": self.product.as_order() if self.product else None,
            "unit": self.unit.as_dict() if self.unit else None,
            "quantity": self.quantity,
            "auto": self.auto,
            "for_breakfast": self.for_breakfast,
            "for_lunch": self.for_lunch,
            "for_dinner": self.for_dinner,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f"<OrderItem(id={self.id}, product_id={self.product_id}, quantity={self.quantity})>"


class MealTimeEnum(enum.Enum):
    BREAKFAST = "BREAKFAST"
    LUNCH = "LUNCH"
    DINNER = "DINNER"


class NoteOrder(Base):
    __tablename__ = "note_orders"

    id = Column(String(255), primary_key=True, default=lambda: str(uuid4()), index=True)
    order_for = Column(String(255), ForeignKey("messs.id", ondelete="CASCADE"), nullable=False)
    order_by = Column(String(255), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(OrderStatusEnum, native_enum=False), default=OrderStatusEnum.PENDING, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = relationship("NoteOrderItem", back_populates="note_order", cascade="all, delete-orphan", lazy="joined")
    mess = relationship("Mess", backref="note_orders")
    user = relationship("User", backref="note_orders")

    def as_dict(self):
        return {
            "id": self.id,
            "status": self.status,
            "items": [item.as_dict() for item in self.items],
            "mess": self.mess.as_dict() if self.mess else None,  # Example: Show mess name
            "user": self.user.as_dict() if self.user else None,   # Example: Show user name
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class NoteOrderItem(Base):
    __tablename__ = "note_order_items"

    id = Column(String(255), primary_key=True, default=lambda: str(uuid4()), index=True)
    order_id = Column(String(255), ForeignKey("note_orders.id", ondelete="CASCADE"), nullable=False)
    meal_time = Column(Enum(MealTimeEnum, native_enum=False), default=MealTimeEnum.BREAKFAST, nullable=False)
    meal_budget = Column(Integer, default=0, nullable=False)
    total_meal = Column(Integer, default=0, nullable=False)
    note = Column(String(500), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    note_order = relationship("NoteOrder", back_populates="items")

    def as_dict(self):
        return {
            "id": self.id,
            "meal_time": self.meal_time,
            "meal_budget": self.meal_budget,
            "total_meal": self.total_meal,
            "note": self.note,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
