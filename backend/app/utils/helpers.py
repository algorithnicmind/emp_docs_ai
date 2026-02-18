"""
Helper Utilities
=================
Common helper functions used across the application.
"""

import os
import uuid
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

import aiofiles
from fastapi import UploadFile
from loguru import logger

from app.config import get_settings

settings = get_settings()


async def save_upload(file: UploadFile, upload_dir: str = None) -> str:
    """
    Save an uploaded file to disk.

    Args:
        file: The uploaded file from FastAPI.
        upload_dir: Override upload directory.

    Returns:
        The absolute file path where the file was saved.
    """
    upload_path = Path(upload_dir or settings.UPLOAD_DIR)
    upload_path.mkdir(parents=True, exist_ok=True)

    # Generate unique filename
    ext = Path(file.filename).suffix
    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_path = upload_path / unique_name

    async with aiofiles.open(file_path, "wb") as f:
        content = await file.read()
        await f.write(content)

    logger.info(f"Saved upload: {file.filename} → {file_path}")
    return str(file_path)


def get_file_extension(filename: str) -> str:
    """Get the lowercase file extension without the dot."""
    return Path(filename).suffix.lower().lstrip(".")


def generate_document_id() -> str:
    """Generate a unique document ID."""
    return str(uuid.uuid4())


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def utcnow() -> datetime:
    """Get current UTC datetime."""
    return datetime.utcnow()
