"""
Database Configuration
======================
Async SQLAlchemy engine, session factory, and Base model.
"""

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings

settings = get_settings()

# ── Async Engine ─────────────────────────────────────────────
# ── Async Engine ─────────────────────────────────────────────
connect_args = {}
if "sqlite" in settings.DATABASE_URL:
    connect_args["check_same_thread"] = False

engine_kwargs = {
    "echo": settings.DEBUG,
    "pool_pre_ping": True,
}

if "sqlite" not in settings.DATABASE_URL:
    engine_kwargs["pool_size"] = 20
    engine_kwargs["max_overflow"] = 10
else:
    engine_kwargs["connect_args"] = connect_args

engine = create_async_engine(
    settings.DATABASE_URL,
    **engine_kwargs
)

# ── Session Factory ──────────────────────────────────────────
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ── Base Model ───────────────────────────────────────────────
class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


# ── Dependency ───────────────────────────────────────────────
async def get_db() -> AsyncSession:
    """FastAPI dependency that provides a database session."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
