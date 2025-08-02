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
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")

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
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", 3306))
    DB_NAME: str = os.getenv("DB_DB", "annoor_mesh")

    # Credentials
    DB_USER: str = os.getenv("DB_USER", "db_admin")
    DB_PASS: str = os.getenv("DB_PASS", "TechNebula_2025")

    LOCAL_DB_USER: str = os.getenv("LOCAL_DB_USER", "root")
    LOCAL_DB_PASS: str = os.getenv("LOCAL_DB_PASS", "Admin_1234")

    # Providers
    DB_PROVIDER_MYSQL: str = os.getenv("DB_PROVIDER_MYSQL", "mysql+pymysql")
    DB_PROVIDER_POSTGRES: str = os.getenv("DB_PROVIDER_POSTGRES", "postgresql+psycopg")

    # Final database URI
    DATABASE_URI: str = (
        f"{DB_PROVIDER_MYSQL}://"
        f"{LOCAL_DB_USER if DEBUG else DB_USER}:"
        f"{LOCAL_DB_PASS if DEBUG else DB_PASS}@"
        f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    UPLOAD_DIR: str = os.path.join(Path(""), "uploads")

    # JWT Config
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "8deadce9449770680910741063cd0a3fe0acb62a8978661f421bbcbb66dc41f1")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 1 hour

    DEFAULT_FAILED_ATTEMPT_TIMEOUT: timedelta = timedelta(minutes=5)

    # ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 2))

    SESSION_COOKIE_KEY: str = os.environ.get("SESSION_COOKIE_KEY", "x-smat-session")

    PROFILE_PICTURE_UPLOAD_DIR: str = os.path.join(UPLOAD_DIR, "profiles")

    # COOKIE SETTINGS
    FRONTEND_COOKIE_DOMAIN: str = ("localhost" if DEBUG else "nuraloom.xyz")
    FRONTEND_ACCESS_COOKIE_KEY: str = "access_token"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
