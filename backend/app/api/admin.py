"""
Admin API Routes
==================
Dashboard statistics, analytics, and user management.
All routes require admin role.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.document import Document
from app.models.chunk import Chunk
from app.models.query_log import QueryLog
from app.services.retrieval import VectorStore

router = APIRouter(prefix="/admin", tags=["Admin"])


# ── Middleware: Admin Only ───────────────────────────────────

async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Dependency that ensures only admins can access."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required",
        )
    return current_user


# ── Routes ───────────────────────────────────────────────────

@router.get("/stats")
async def get_dashboard_stats(
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Get overview statistics for the admin dashboard."""

    # Total documents
    doc_count = await db.execute(
        select(func.count(Document.id)).where(Document.status != "deleted")
    )
    total_docs = doc_count.scalar() or 0

    # Total chunks
    chunk_count = await db.execute(select(func.count(Chunk.id)))
    total_chunks = chunk_count.scalar() or 0

    # Total queries
    query_count = await db.execute(select(func.count(QueryLog.id)))
    total_queries = query_count.scalar() or 0

    # Total users
    user_count = await db.execute(
        select(func.count(User.id)).where(User.is_active == True)
    )
    total_users = user_count.scalar() or 0

    # Average feedback score
    avg_feedback = await db.execute(
        select(func.avg(QueryLog.feedback_score)).where(
            QueryLog.feedback_score.isnot(None)
        )
    )
    avg_score = avg_feedback.scalar()

    # Average response time
    avg_time = await db.execute(
        select(func.avg(QueryLog.response_time_ms)).where(
            QueryLog.response_time_ms.isnot(None)
        )
    )
    avg_response_time = avg_time.scalar()

    # Vector store stats
    try:
        vs = VectorStore()
        vs_stats = vs.get_stats()
        vector_count = vs_stats["total_chunks"]
    except Exception:
        vector_count = 0

    return {
        "total_documents": total_docs,
        "total_chunks": total_chunks,
        "total_queries": total_queries,
        "total_users": total_users,
        "total_vectors": vector_count,
        "avg_feedback_score": round(avg_score, 2) if avg_score else None,
        "avg_response_time_ms": round(avg_response_time) if avg_response_time else None,
    }


@router.get("/analytics/top-questions")
async def get_top_questions(
    limit: int = 10,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Get the most frequently asked questions."""
    result = await db.execute(
        select(
            QueryLog.question,
            func.count(QueryLog.id).label("count"),
            func.avg(QueryLog.feedback_score).label("avg_score"),
        )
        .group_by(QueryLog.question)
        .order_by(desc("count"))
        .limit(limit)
    )

    top_questions = [
        {
            "question": row.question,
            "count": row.count,
            "avg_score": round(row.avg_score, 2) if row.avg_score else None,
        }
        for row in result.all()
    ]

    return {"top_questions": top_questions}


@router.get("/analytics/recent-queries")
async def get_recent_queries(
    limit: int = 20,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Get the most recent queries."""
    result = await db.execute(
        select(QueryLog)
        .order_by(QueryLog.timestamp.desc())
        .limit(limit)
    )
    queries = result.scalars().all()

    return {
        "queries": [
            {
                "id": str(q.id),
                "question": q.question,
                "response_time_ms": q.response_time_ms,
                "feedback_score": q.feedback_score,
                "model_used": q.model_used,
                "tokens_used": q.tokens_used,
                "timestamp": q.timestamp.isoformat() if q.timestamp else None,
            }
            for q in queries
        ]
    }


@router.get("/users")
async def list_users(
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """List all users."""
    result = await db.execute(
        select(User).order_by(User.created_at.desc())
    )
    users = result.scalars().all()

    return {
        "users": [
            {
                "id": str(u.id),
                "name": u.name,
                "email": u.email,
                "role": u.role,
                "department": u.department,
                "is_active": u.is_active,
                "created_at": u.created_at.isoformat() if u.created_at else None,
            }
            for u in users
        ]
    }


class UpdateRoleRequest(BaseModel):
    role: str


@router.put("/users/{user_id}/role")
async def update_user_role(
    user_id: str,
    request: UpdateRoleRequest,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Update a user's role."""
    valid_roles = ["admin", "hr", "engineering", "finance", "general"]
    if request.role not in valid_roles:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid role. Must be one of: {', '.join(valid_roles)}",
        )

    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = request.role

    return {
        "message": f"User '{user.name}' role updated to '{request.role}'",
    }
