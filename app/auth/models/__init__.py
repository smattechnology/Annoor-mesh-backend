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


class RoleEnum(enum.Enum):
    ADMIN = "admin"
    USER = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(String(255), primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER, nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.ACTIVE, nullable=False)
    allocated_mess_id = Column(String(255), ForeignKey("messs.id"))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    emails = relationship("Email", backref="user", cascade="all, delete-orphan")
    info = relationship("Info", backref="user", uselist=False, cascade="all, delete-orphan")
    passwords = relationship("Password", backref="user", cascade="all, delete-orphan")
    mess = relationship("Mess", back_populates="users", uselist=False)

    def active_password(self):
        return next((p for p in self.passwords if p.status == StatusEnum.ACTIVE), None)

    def active_email(self):
        return next((e for e in self.emails if e.status == StatusEnum.ACTIVE), None)

    def as_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.active_email().email if self.active_email() else None,
            "name": self.info.name if self.info else None,
            "role": self.role.value if self.role else None,
            "status": self.status.value if self.status else None,
            "dob": self.info.dob.isoformat() if self.info and self.info.dob else None,
            "allocated_mess": self.mess.as_dict() if self.mess else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(255), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    status = Column(Enum(StatusEnum), default=StatusEnum.ACTIVE, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Info(Base):
    __tablename__ = "infos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(255), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    name = Column(String(255), nullable=True)
    firstMame = Column(String(255), nullable=True)
    middleName = Column(String(255), nullable=True)
    lastName = Column(String(255), nullable=True)
    dob = Column(Date, nullable=True)
    address = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Password(Base):
    __tablename__ = "passwords"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(255), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    password = Column(String(255), nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.ACTIVE, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
