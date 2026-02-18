"""
Logger Configuration
======================
Structured logging using loguru.
"""

import sys
from loguru import logger

from app.config import get_settings

settings = get_settings()

# Remove default logger
logger.remove()

# Console output — colorful, with timestamps
logger.add(
    sys.stdout,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    ),
    level="DEBUG" if settings.DEBUG else "INFO",
    colorize=True,
)

# File output — rotated daily, retained 30 days
logger.add(
    "logs/app_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="30 days",
    compression="zip",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
)

__all__ = ["logger"]
