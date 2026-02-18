"""
Query Log Model
===============
Tracks every user query for analytics and feedback.
"""

import uuid
from datetime import datetime

from sqlalchemy import (
    Column, String, Integer, Float, DateTime, Text, ForeignKey
)
from sqlalchemy import Uuid, JSON
from sqlalchemy.orm import relationship

from app.database import Base


class QueryLog(Base):
    __tablename__ = "query_logs"

    id = Column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    user_id = Column(
        Uuid,
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )
    question = Column(Text, nullable=False)
    response = Column(Text, nullable=True)
    sources_used = Column(JSON, nullable=True)
    similarity_score = Column(Float, nullable=True)
    response_time_ms = Column(Integer, nullable=True)
    feedback_score = Column(Integer, nullable=True, index=True)  # -1 or 1
    model_used = Column(String(50), nullable=True)
    tokens_used = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="query_logs")

    def __repr__(self):
        return f"<QueryLog '{self.question[:50]}...'>"
