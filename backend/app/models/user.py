"""
User Model
==========
Represents system users with role-based access control.
Roles: admin, hr, engineering, finance, general
"""

import uuid
from datetime import datetime

from sqlalchemy import (
    Column, String, Boolean, DateTime, Text
)
from sqlalchemy import Uuid
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(
        String(50),
        nullable=False,
        default="general",
        index=True,
    )
    department = Column(String(100), default="general")
    slack_id = Column(String(50), unique=True, nullable=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    query_logs = relationship(
        "QueryLog", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.name} ({self.role})>"
