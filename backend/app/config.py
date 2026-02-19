"""
Configuration Management
========================
Centralized settings using pydantic-settings.
All values are loaded from environment variables / .env file.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # ── Application ──────────────────────────────────────────
    APP_ENV: str = "development"
    APP_PORT: int = 8000
    APP_HOST: str = "0.0.0.0"
    DEBUG: bool = True

    # ── Database (PostgreSQL) ────────────────────────────────
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres123@localhost:5432/emp_docs_ai"
    DATABASE_URL_SYNC: str = "postgresql://postgres:postgres123@localhost:5432/emp_docs_ai"

    # ── Redis ────────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379"

    # ── OpenAI ───────────────────────────────────────────────
    OPENAI_API_KEY: str = ""

    # ── JWT Authentication ───────────────────────────────────
    JWT_SECRET_KEY: str = "super-secret-jwt-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

    # ── Slack ────────────────────────────────────────────────
    SLACK_BOT_TOKEN: str = ""
    SLACK_SIGNING_SECRET: str = ""
    SLACK_APP_TOKEN: str = ""

    # ── Vector Store ─────────────────────────────────────────
    VECTOR_STORE_PATH: str = "./vector_store"
    VECTOR_STORE_TYPE: str = "chroma"  # "chroma" or "faiss"

    # ── Embedding Model ──────────────────────────────────────
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    EMBEDDING_DIMENSIONS: int = 1536

    # ── LLM Model ────────────────────────────────────────────
    LLM_MODEL: str = "gpt-4"
    LLM_TEMPERATURE: float = 0.1
    LLM_MAX_TOKENS: int = 1000

    # ── Chunking ─────────────────────────────────────────────
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 100

    # ── Query ────────────────────────────────────────────────
    TOP_K_RESULTS: int = 5
    SIMILARITY_THRESHOLD: float = 0.7

    # ── Upload ───────────────────────────────────────────────
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE_MB: int = 50

    model_config = {
        "env_file": "../.env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "ignore",
    }


@lru_cache()
def get_settings() -> Settings:
    """Cached settings singleton."""
    return Settings()
