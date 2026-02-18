"""
FastAPI Application Entry Point
==================================
The main application factory: configures middleware, routes, and startup events.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.config import get_settings
from app.database import engine, Base
from app.api import auth, query, documents, admin

settings = get_settings()


# ── Lifespan ─────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    logger.info("🚀 Starting Internal Docs Q&A Agent...")

    # Create database tables (only for development)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("✅ Database tables created/verified")
    logger.info(f"📡 API running at http://{settings.APP_HOST}:{settings.APP_PORT}")
    logger.info(f"📚 API Docs at http://localhost:{settings.APP_PORT}/docs")

    yield

    logger.info("👋 Shutting down...")
    await engine.dispose()


# ── App Factory ──────────────────────────────────────────────

app = FastAPI(
    title="Internal Docs Q&A Agent",
    description=(
        "AI-powered assistant that aggregates internal documents, "
        "understands natural language queries using semantic search, "
        "and provides citation-backed answers with role-based access control."
    ),
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


# ── CORS Middleware ──────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Rate Limiting ────────────────────────────────────────────

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.responses import JSONResponse

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={
            "error": "rate_limited",
            "message": "Too many requests. Please try again later.",
        },
    )


# ── Register API Routes ─────────────────────────────────────

API_PREFIX = "/api/v1"

app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(query.router, prefix=API_PREFIX)
app.include_router(documents.router, prefix=API_PREFIX)
app.include_router(admin.router, prefix=API_PREFIX)


# ── Health Check ─────────────────────────────────────────────

@app.get("/", tags=["Health"])
async def root():
    return {
        "name": "Internal Docs Q&A Agent",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.APP_ENV,
    }
