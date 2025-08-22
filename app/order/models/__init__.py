import enum
from uuid import uuid4
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    DateTime,
    Integer,
    Boolean,
    Enum,
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

    order_for = Column(String(255), ForeignKey("messs.id"))  # fixed typo here
    order_by = Column(String(255), ForeignKey("users.id"))

    meal_budget = Column(Integer, nullable=False)
    total_meal = Column(Integer, nullable=False)

    status = Column(
        Enum(OrderStatusEnum), default=OrderStatusEnum.PENDING, nullable=False
    )

    items = relationship(
        "OrderItem", backref="order", cascade="all, delete-orphan", lazy="joined"
    )

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def as_dict(self):
        return {
            "id": self.id,
            "order_for": self.order_for,
            "order_by": self.order_by,
            "meal_budget": self.meal_budget,
            "total_meal": self.total_meal,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "items": [item.as_dict() for item in self.items],
        }


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(String(255), primary_key=True, default=lambda: str(uuid4()), index=True)

    order_id = Column(String(255), ForeignKey("orders.id"))
    product_id = Column(String(255), ForeignKey("products.id"))
    unit_id = Column(String(255), ForeignKey("items_unit.id"))

    auto = Column(Boolean,default=True,nullable=False)
    quantity= Column(Integer,default=0,nullable=False)

    for_breakfast = Column(Boolean, nullable=False, default=False)
    for_lunch = Column(Boolean, nullable=False, default=False)
    for_dinner = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def as_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "unit_id": self.unit_id,
            "quantity": self.quantity,
            "auto": self.auto,
            "for_breakfast": self.for_breakfast,
            "for_lunch": self.for_lunch,
            "for_dinner": self.for_dinner,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
