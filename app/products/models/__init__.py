from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database.base import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(String(255), primary_key=True, index=True)
    label = Column(String(255), nullable=False)
    icon = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    products = relationship("Product", back_populates="category", cascade="all, delete")

    def as_dict(self):
        return {
            "id": self.id,
            "label": self.label,
            "icon": self.icon,
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

    products = relationship("Product", back_populates="unite", cascade="all, delete")

    def as_dict(self):
        return {
            "id": self.id,
            "label": self.label,
            "icon": self.icon,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class Product(Base):
    __tablename__ = "products"

    id = Column(String(255), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)

    category_id = Column(String(255), ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    unit_id = Column(String(255), ForeignKey("unites.id", ondelete="CASCADE"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = relationship("Category", back_populates="products")
    unite = relationship("Unite", back_populates="products")

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "category": self.category.as_dict(),
            "unit": self.unite.as_dict(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
