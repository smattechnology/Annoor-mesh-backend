from datetime import datetime
from sqlalchemy import Column, String, Enum, ForeignKey, DateTime, Integer, Boolean, Date
from sqlalchemy.orm import relationship
from app.database.base import Base
import enum


class Category(Base):
    __tablename__ = "categories"

    id = Column(String(255), primary_key=True, index=True)

    value = Column(String(255), nullable=False)
    label = Column(String(255), nullable=False)
    icon = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def as_dict(self):
        return {
            "id": self.id,

            "value": self.value if self.value else None,
            "label": self.label if self.label else None,
            "icon": self.icon if self.icon else None,

            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class Unite(Base):
    __tablename__ = "unites"

    id = Column(String(255), primary_key=True, index=True)

    value = Column(String(255), nullable=False)
    label = Column(String(255), nullable=False)
    icon = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def as_dict(self):
        return {
            "id": self.id,

            "value": self.value if self.value else None,
            "label": self.label if self.label else None,
            "icon": self.icon if self.icon else None,

            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class Product(Base):
    __tablename__ = "prodicts"

    id = Column(String(255), primary_key=True, index=True)

    name = Column(String(255), nullable=False)
    price = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)

    category_id = Column(String(255), ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    unite_id = Column(String(255), ForeignKey("unites.id", ondelete="CASCADE"), nullable=False)


    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = relationship("Category", backref="product", uselist=False, cascade="all, delete-orphan")
    unite = relationship("Unite", backref="product", uselist=False, cascade="all, delete-orphan")


    def as_dict(self):
        return {
            "id": self.id,

            "name": self.name if self.name else None,
            "price": self.price if self.price else None,
            "description": self.description if self.description else None,
            "category_id": self.category_id if self.category_id else None,
            "unite_id": self.unite_id if self.unite_id else None,

            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }