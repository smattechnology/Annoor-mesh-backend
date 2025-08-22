import re
import datetime
from datetime import timedelta
from typing import Optional

from pydantic import EmailStr

from app.settings import settings
from jose import jwt, JWTError

def is_email(value: str) -> bool:
    return re.match(r"[^@]+@[^@]+\.[^@]+", value) is not None


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    expire = datetime.datetime.now(datetime.UTC) + (expires_delta or timedelta(days=30))
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

def generate_username(email: EmailStr or str) -> str:
    return email.split('@')[0]

class NameParser:
    def __init__(self, full_name: str):
        self.fullname: str = full_name.strip()
        parts = self.fullname.split()

        self.first_name: str = parts[0] if parts else ""
        self.middle_name: str | None = None
        self.last_name: str = ""

        if len(parts) == 2:
            self.last_name = parts[1]
        elif len(parts) >= 3:
            self.middle_name = " ".join(parts[1:-1])
            self.last_name = parts[-1]

    def get_full_name(self) -> str:
        return self.fullname

    def get_first_name(self) -> str:
        return self.first_name

    def get_middle_name(self) -> Optional[str]:
        return self.middle_name

    def get_last_name(self) -> str:
        return self.last_name

    def get_dot_name(self) -> str:
        return ".".join(
            part.lower()
            for part in [self.first_name, self.middle_name, self.last_name]
            if part
        )
