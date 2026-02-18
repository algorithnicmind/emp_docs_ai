"""
Document Model
==============
Represents an ingested document with metadata.
Tracks source, department, access level, and processing status.
"""

import uuid
from datetime import datetime

from sqlalchemy import (
    Column, String, Integer, DateTime, Text
)
from sqlalchemy import Uuid
from sqlalchemy.orm import relationship

from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    title = Column(String(500), nullable=False)
    source = Column(String(50), nullable=False, index=True)          # pdf_upload, markdown, notion, etc.
    department = Column(String(100), nullable=False, default="general", index=True)
    access_level = Column(String(50), nullable=False, default="all", index=True)  # all, department, confidential
    author = Column(String(255), nullable=True)
    file_type = Column(String(20), nullable=True)                    # pdf, md, html, txt
    file_path = Column(Text, nullable=True)
    source_url = Column(Text, nullable=True)
    word_count = Column(Integer, nullable=True)
    chunk_count = Column(Integer, default=0)
    status = Column(
        String(20), default="processing", index=True
    )  # processing, indexed, failed, deleted
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    chunks = relationship(
        "Chunk",
        back_populates="document",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Document '{self.title}' ({self.source})>"
