from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Enum,
    ForeignKey,
    DateTime,
    Integer, Boolean, Date
)
from sqlalchemy.orm import relationship
from app.database.base import Base
import enum


class StatusEnum(enum.Enum):
    ACTIVE = "active"
    DISABLED = "disabled"
    DELETED = "deleted"
    BANNED = "banned"


class Mess(Base):
    __tablename__ = "messs"

    id = Column(String(255), primary_key=True, index=True)

    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=True)

    status = Column(Enum(StatusEnum), default=StatusEnum.ACTIVE, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "phone": self.phone,
            "status": self.status.value if self.status else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
