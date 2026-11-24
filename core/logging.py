"""
Enterprise Logging Module for TalentSphere Enterprise 2.0.
Provides structured, rotating file logging and console output.
"""
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from core.config import settings

LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

root_logger = logging.getLogger("talentsphere")
if not root_logger.handlers:
    numeric_level = getattr(logging, settings.LOG_LEVEL, logging.INFO)
    root_logger.setLevel(numeric_level)
    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    # 1. Rotating File Handler (Max 10 MB per file, keep 5 backups)
    log_file = settings.LOGS_DIR / "talentsphere_enterprise.log"
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(numeric_level)
    root_logger.addHandler(file_handler)

    # 2. Console Stream Handler
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.WARNING if not settings.DEBUG else numeric_level)
    root_logger.addHandler(stream_handler)

def get_logger(module_name: str) -> logging.Logger:
    """Returns a module-scoped logger."""
    return logging.getLogger(f"talentsphere.{module_name}")
