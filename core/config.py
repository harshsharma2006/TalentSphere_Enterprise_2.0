"""
Core Configuration Module for TalentSphere Enterprise 2.0.
Loads settings from environment variables and provides centralized application configuration.
"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Base Directory: TalentSphere_Enterprise_2.0
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

class Settings:
    """Enterprise application settings container."""

    # Application Metadata
    APP_ENV: str = os.getenv("APP_ENV", "development").lower()
    APP_NAME: str = os.getenv("APP_NAME", "TalentSphere Enterprise 2.0")
    APP_VERSION: str = os.getenv("APP_VERSION", "2.0.0")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")

    # Directory Paths
    BASE_DIR: Path = BASE_DIR
    UPLOAD_DIR: Path = BASE_DIR / "uploads" / "resumes"
    LOGS_DIR: Path = BASE_DIR / "logs"
    REPORTS_DIR: Path = BASE_DIR / "reports" / "generated"

    # Database Configuration
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'talentsphere_enterprise.db'}"
    )

    # Security & Cryptography
    SECRET_KEY: str = os.getenv("SECRET_KEY", "talentsphere-enterprise-2.0-secure-secret-key-2026")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
    PASSWORD_BCRYPT_ROUNDS: int = int(os.getenv("PASSWORD_BCRYPT_ROUNDS", "12"))

    # Initial Provisioning
    INITIAL_ADMIN_EMAIL: str = os.getenv("INITIAL_ADMIN_EMAIL", "superadmin@talentsphere.local")
    INITIAL_ADMIN_USERNAME: str = os.getenv("INITIAL_ADMIN_USERNAME", "superadmin")
    INITIAL_ADMIN_PASSWORD: str = os.getenv("INITIAL_ADMIN_PASSWORD", "SuperAdmin@2026")

    # Server Configuration
    SERVER_HOST: str = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "8501"))

    # AI Engine Configuration
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "local_fallback").lower()
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")

    # Operational Limits
    MAX_UPLOAD_SIZE_MB: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "25"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()

    def __init__(self):
        # Ensure runtime folders exist
        self.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        self.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        self.REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    @property
    def is_sqlite(self) -> bool:
        return self.DATABASE_URL.startswith("sqlite")

settings = Settings()
