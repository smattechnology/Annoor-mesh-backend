import random
from datetime import datetime

from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Enum, Boolean
from sqlalchemy.orm import relationship
from app.database.base import Base
import enum


class RandomSelectEnum(enum.Enum):
    STATIC = "STATIC"
    DYNAMIC = "DYNAMIC"


class Category(Base):
    __tablename__ = "categories"

    id = Column(String(255), primary_key=True, index=True)
    label = Column(String(255), nullable=False)
    icon = Column(String(255), nullable=True)
    rand_select = Column(Enum(RandomSelectEnum), default=RandomSelectEnum.STATIC, nullable=False)

    min = Column(Integer, default=2)
    max = Column(Integer, default=5)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    products = relationship("Product", back_populates="category", cascade="all, delete")

    def as_random(self):
        """
        Returns a dict representation of the category with random products.
        - STATIC → always 1 random product
        - DYNAMIC → random number between min & max (capped by total products)
        """
        selected_products = []

        if self.products:
            if self.rand_select == RandomSelectEnum.STATIC:
                # Always return exactly one product
                selected_products = [random.choice(self.products)]
            else:  # DYNAMIC
                total = len(self.products)

                # Clamp min/max to available product count
                min_n = min(self.min, total)
                max_n = min(self.max, total)

                # Pick a random number of products between min_n and max_n
                n = random.randint(min_n, max_n) if max_n > 0 else 0

                selected_products = random.sample(self.products, n)

        return {
            "id": self.id,
            "label": self.label,
            "icon": self.icon,
            "products": [product.as_dict() for product in selected_products],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def as_category(self):
        return {
            "id": self.id,
            "label": self.label,
            "icon": self.icon,
            "rand_select": self.rand_select,
            "min": self.min,
            "max": self.max,
            "products": [product.as_dict() for product in self.products] if self.products else [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def as_dict(self):
        return {
            "id": self.id,
            "label": self.label,
            "icon": self.icon,
            "rand_select": self.rand_select,
            "min": self.min,
            "max": self.max,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class Product(Base):
    __tablename__ = "products"

    id = Column(String(255), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)

    category_id = Column(String(255), ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = relationship("Category", back_populates="products")
    items_unit = relationship("ItemUnit", back_populates="products", cascade="all, delete-orphan")

    def get_unit(self):
        """Return the generic/default unit if available"""
        for i in self.items_unit:
            if i.is_generic:
                return i.as_dict()
        return None

    def to_category(self):
        unit = self.get_unit()
        return {
            "id": self.id,
            "name": self.name,
            "price": unit["price"] if unit else None,
            "unit": unit,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category.as_dict(),
            "units": [iu.as_dict() for iu in self.items_unit],
            "unit": self.get_unit(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class Unite(Base):
    __tablename__ = "unites"

    id = Column(String(255), primary_key=True, index=True)
    label = Column(String(255), nullable=False)
    icon = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    items_unit = relationship("ItemUnit", back_populates="unit", cascade="all, delete")

    def as_dict(self):
        return {
            "id": self.id,
            "label": self.label,
            "icon": self.icon,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class ItemUnit(Base):
    __tablename__ = "items_unit"

    id = Column(String(255), primary_key=True, index=True)
    product_id = Column(String(255), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)

    unit_id = Column(String(255), ForeignKey("unites.id", ondelete="CASCADE"), nullable=False)

    price = Column(Integer, nullable=False)

    is_generic = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    unit = relationship("Unite", back_populates="items_unit")
    products = relationship("Product", back_populates="items_unit")

    def as_dict(self):
        return {
            "id": self.id,
            "icon": self.unit.icon,
            "label": self.unit.label,
            "price": self.price,
            "is_generic": self.is_generic,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
