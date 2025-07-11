import os
from typing import Optional


class Settings:
    PROJECT_NAME: str = "FastFluence"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./fastfluence.db")

    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:8080",
        "https://fastfluence.home.lineofcode.pl",
        "https://api.fastfluence.home.lineofcode.pl",
        # Development
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]


settings = Settings()