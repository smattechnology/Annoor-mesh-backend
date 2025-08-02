import os
from datetime import timedelta

from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any, List
import secrets
from pydantic import AnyHttpUrl
from pathlib import Path
from dotenv import load_dotenv

env_path = Path("") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    # App
    APP_NAME: str = os.environ.get("APP_NAME", "FastAPI")
    DEBUG: bool = bool(os.environ.get("DEBUG", False))
    API_V1_STR: str = "/api/v1"

    # FrontEnd Application
    FRONTEND_HOST: str = os.environ.get("FRONTEND_HOST", "http://localhost:3000")

    ORIGINS: list[str] = (
        [
            "http://localhost:3000",
            "http://localhost:3001",
        ] if DEBUG else [
            "https://frontend.nuraloom.xyz",
            "https://annoor.nuraloom.xyz",
        ]
    )

    # Database Config
    DB_HOST: str = os.environ.get("DB_HOST", 'localhost')
    DB_USER: str = os.environ.get("DB_USER", 'db_admin')
    DB_PASS: str = os.environ.get("DB_PASS", 'TechNebula_2025')
    DB_PORT: int = int(os.environ.get("DB_PORT", 3306))
    DB_DB: str = os.environ.get("DB_DB", 'annoor_mesh')
    DB_PROVIDER_MYSQL: str = os.environ.get("DP_PROVIDER_MYSQL", "mysql+pymysql")
    DB_PROVIDER_POSTGRES: str = os.environ.get("DP_PROVIDER_MYSQL", "postgresql+psycopg")
    DATABASE_URI: str = f"{DB_PROVIDER_MYSQL}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_DB}"

    UPLOAD_DIR: str = os.path.join(Path(""), "uploads")

    # JWT Config
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "8deadce9449770680910741063cd0a3fe0acb62a8978661f421bbcbb66dc41f1")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 1 hour

    DEFAULT_FAILED_ATTEMPT_TIMEOUT: timedelta = timedelta(minutes=5)

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 2))

    SESSION_COOKIE_KEY: str = os.environ.get("SESSION_COOKIE_KEY", "x-smat-session")

    PROFILE_PICTURE_UPLOAD_DIR: str = os.path.join(UPLOAD_DIR, "profiles")

    # COOKIE SETTINGS
    FRONTEND_COOKIE_DOMAIN:str = ("localhost" if DEBUG else "nuraloom.xyz")
    FRONTEND_ACCESS_COOKIE_KEY:str = "access_token"


    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
