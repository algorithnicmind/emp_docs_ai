"""
Data Source Model
=================
Represents external data sources (Notion, Google Docs, Confluence, etc.)
for scheduled or webhook-based syncing.
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy import Uuid, JSON

from app.database import Base


class DataSource(Base):
    __tablename__ = "data_sources"

    id = Column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)        # notion, google_docs, confluence
    config = Column(JSON, nullable=True)             # Connection config (encrypted)
    last_sync = Column(DateTime, nullable=True)
    status = Column(String(20), default="active")     # active, paused, error
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<DataSource '{self.name}' ({self.type})>"
