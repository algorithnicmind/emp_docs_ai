"""
Query API Routes
==================
Handles user questions — processes through the RAG pipeline
and returns citation-backed answers.
"""

import json
import time

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.query_log import QueryLog
from app.services.query_pipeline import QueryPipeline
from app.config import get_settings

settings = get_settings()
router = APIRouter(prefix="/query", tags=["Query"])

# Initialize the pipeline (singleton)
pipeline = None


def get_pipeline() -> QueryPipeline:
    """Lazy-initialize the query pipeline."""
    global pipeline
    if pipeline is None:
        pipeline = QueryPipeline()
    return pipeline


# ── Schemas ──────────────────────────────────────────────────

class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = None


class FeedbackRequest(BaseModel):
    query_id: str
    score: int  # -1 or 1
    comment: Optional[str] = None


# ── Routes ───────────────────────────────────────────────────

@router.post("")
async def ask_question(
    request: QueryRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Ask a question and get an AI-generated, citation-backed answer.
    The response includes the answer, source documents, and confidence level.
    """
    qp = get_pipeline()

    result = await qp.process(
        question=request.question,
        user_id=str(current_user.id),
        user_role=current_user.role,
        top_k=request.top_k,
    )

    # Log query to database
    log = QueryLog(
        user_id=current_user.id,
        question=request.question,
        response=result["answer"],
        sources_used=result["sources"],
        similarity_score=result.get("top_similarity_score"),
        response_time_ms=result["response_time_ms"],
        model_used=result.get("model"),
        tokens_used=result.get("tokens_used", {}).get("total"),
    )
    db.add(log)

    return result


@router.post("/stream")
async def ask_question_stream(
    request: QueryRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Ask a question and receive a streaming response via Server-Sent Events.
    Each chunk of the answer is sent as it's generated.
    """
    qp = get_pipeline()

    async def event_stream():
        async for token in qp.process_stream(
            question=request.question,
            user_id=str(current_user.id),
            user_role=current_user.role,
            top_k=request.top_k,
        ):
            yield f"data: {json.dumps({'token': token})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
    )


@router.post("/feedback")
async def submit_feedback(
    request: FeedbackRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Submit feedback (helpful / not helpful) for a query response."""
    from sqlalchemy import select

    result = await db.execute(
        select(QueryLog).where(QueryLog.id == request.query_id)
    )
    log = result.scalar_one_or_none()

    if not log:
        raise HTTPException(status_code=404, detail="Query not found")

    log.feedback_score = request.score

    return {"status": "success", "message": "Feedback recorded"}
