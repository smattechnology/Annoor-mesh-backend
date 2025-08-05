from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Enum,
    ForeignKey,
    DateTime,
    Integer,
)
from sqlalchemy.orm import relationship
from app.database.base import Base
import enum


class StatusEnum(enum.Enum):
    ACTIVE = "active"
    DISABLED = "disabled"
    DELETED = "deleted"
    BANNED = "banned"


class MessTypeEnum(enum.Enum):
    BOYS_MESS = "BOYS_MESS"
    GIRLS_MESS = "GIRLS_MESS"


class Mess(Base):
    __tablename__ = "messs"

    id = Column(String(255), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=True)

    address_id = Column(String(255), ForeignKey("mess_addresses.id", ondelete="CASCADE"), unique=True)
    owner_id = Column(String(255), ForeignKey("mess_owners.id", ondelete="CASCADE"), unique=True)

    status = Column(Enum(StatusEnum), default=StatusEnum.ACTIVE, nullable=False)
    type = Column(Enum(MessTypeEnum), default=MessTypeEnum.BOYS_MESS, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    address = relationship("MessAddress", back_populates="mess", uselist=False)
    mess_owner = relationship("MessOwner", back_populates="mess", uselist=False)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "status": self.status.value if self.status else None,
            "type": self.type.value if self.type else None,
            "address": self.address.as_dict() if self.address else None,
            "owner": self.mess_owner.as_dict() if self.mess_owner else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class MessOwner(Base):
    __tablename__ = "mess_owners"

    id = Column(String(255), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=False)

    mess = relationship("Mess", back_populates="mess_owner", uselist=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class MessAddress(Base):
    __tablename__ = "mess_addresses"

    id = Column(String(255), primary_key=True, index=True)
    street = Column(String(255), nullable=False)
    area = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    postalCode = Column(Integer, nullable=False)

    mess = relationship("Mess", back_populates="address", uselist=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def as_dict(self):
        return {
            "id": self.id,
            "street": self.street,
            "area": self.area,
            "city": self.city,
            "postalCode": self.postalCode,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
