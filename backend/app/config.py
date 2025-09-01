import os
from typing import Optional


class Settings:
    PROJECT_NAME: str = "FastFluence"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ACTIVATION_TOKEN_EXPIRE_HOURS: int = 24

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./fastfluence.db")

    # Frontend URL for email links
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")

    # Email Configuration - SendGrid or SMTP
    USE_SENDGRID_API: bool = os.getenv("USE_SENDGRID_API", "false").lower() == "true"
    SENDGRID_API_KEY: str = os.getenv("SENDGRID_API_KEY", "")

    # SMTP Configuration (fallback or alternative)
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.sendgrid.net")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "apikey")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")  # SendGrid API Key for SMTP
    SMTP_FROM_EMAIL: str = os.getenv("SMTP_FROM_EMAIL", "noreply@fastfluence.pl")

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