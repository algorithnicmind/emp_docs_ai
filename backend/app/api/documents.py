"""
Documents API Routes
======================
Handles document upload, listing, and deletion.
Upload triggers the full ingestion pipeline: parse → chunk → embed → store.
"""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.document import Document
from app.models.chunk import Chunk
from app.services.ingestion import get_ingester
from app.services.chunking import process_text
from app.services.embedding import EmbeddingService
from app.services.retrieval import VectorStore
from app.utils.helpers import save_upload
from app.config import get_settings
from loguru import logger

settings = get_settings()
router = APIRouter(prefix="/documents", tags=["Documents"])


# ── Schemas ──────────────────────────────────────────────────

class DocumentResponse(BaseModel):
    id: str
    title: str
    source: str
    department: str
    access_level: str
    status: str
    chunk_count: int
    word_count: Optional[int] = None
    created_at: str

    class Config:
        from_attributes = True


# ── Routes ───────────────────────────────────────────────────

@router.get("")
async def list_documents(
    page: int = 1,
    limit: int = 20,
    department: Optional[str] = None,
    source: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all documents accessible to the current user."""
    query = select(Document).where(Document.status != "deleted")

    if department:
        query = query.where(Document.department == department)
    if source:
        query = query.where(Document.source == source)

    # Apply RBAC: non-admins only see documents they can access
    if current_user.role != "admin":
        from app.services.rbac import RBACService
        rbac = RBACService()
        # For list view, show public + own department docs
        if current_user.role in ["hr", "engineering", "finance"]:
            query = query.where(
                (Document.access_level == "all") |
                (
                    (Document.access_level == "department") &
                    (Document.department == current_user.department)
                )
            )
        else:
            query = query.where(Document.access_level == "all")

    # Pagination
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit).order_by(Document.created_at.desc())

    result = await db.execute(query)
    documents = result.scalars().all()

    # Get total count
    count_query = select(func.count(Document.id)).where(Document.status != "deleted")
    count_result = await db.execute(count_query)
    total = count_result.scalar()

    return {
        "documents": [
            {
                "id": str(doc.id),
                "title": doc.title,
                "source": doc.source,
                "department": doc.department,
                "access_level": doc.access_level,
                "status": doc.status,
                "chunk_count": doc.chunk_count or 0,
                "word_count": doc.word_count,
                "created_at": doc.created_at.isoformat() if doc.created_at else None,
            }
            for doc in documents
        ],
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit if total else 0,
    }


@router.post("/upload", status_code=201)
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    department: str = Form("general"),
    access_level: str = Form("all"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Upload and index a new document.
    Triggers the full pipeline: parse → chunk → embed → vector store.
    Requires admin or department lead role.
    """
    # Check permissions
    if current_user.role not in ["admin", "hr", "engineering", "finance"]:
        raise HTTPException(
            status_code=403,
            detail="Only admins and department leads can upload documents",
        )

    # Validate access_level
    if access_level not in ["all", "department", "confidential"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid access_level. Must be: all, department, confidential",
        )

    try:
        # Step 1: Save file
        file_path = await save_upload(file)

        # Step 2: Ingest (extract text)
        ingester = get_ingester(file_path=file.filename)
        unified_doc = ingester.ingest(file_path, {
            "title": title,
            "department": department,
            "access_level": access_level,
            "author": current_user.name,
        })

        # Step 3: Create document record
        doc = Document(
            title=title,
            source=unified_doc.metadata.source,
            department=department,
            access_level=access_level,
            author=current_user.name,
            file_type=unified_doc.metadata.file_type,
            file_path=file_path,
            word_count=unified_doc.metadata.word_count,
            status="processing",
        )
        db.add(doc)
        await db.flush()
        await db.refresh(doc)

        doc_id = str(doc.id)

        # Step 4: Chunk text
        chunks = process_text(unified_doc.raw_text, doc_id)

        # Step 5: Generate embeddings
        embedding_service = EmbeddingService()
        chunk_texts = [c["chunk_text"] for c in chunks]
        embeddings = embedding_service.embed_batch(chunk_texts)

        # Step 6: Store in vector DB
        vector_store = VectorStore()
        vector_store.add_chunks(
            chunks=chunks,
            embeddings=embeddings,
            doc_metadata={
                "department": department,
                "access_level": access_level,
                "title": title,
                "source": unified_doc.metadata.source,
            },
        )

        # Step 7: Save chunks to PostgreSQL
        for chunk in chunks:
            db_chunk = Chunk(
                document_id=doc.id,
                chunk_text=chunk["chunk_text"],
                chunk_index=chunk["chunk_index"],
                embedding_ref=chunk["chunk_id"],
                token_count=chunk["token_count"],
            )
            db.add(db_chunk)

        # Update document status
        doc.chunk_count = len(chunks)
        doc.status = "indexed"

        logger.info(
            f"Document '{title}' indexed: {len(chunks)} chunks, "
            f"{len(embeddings)} embeddings"
        )

        return {
            "id": doc_id,
            "title": title,
            "status": "indexed",
            "chunk_count": len(chunks),
            "message": f"Document indexed successfully with {len(chunks)} chunks",
        }

    except Exception as e:
        logger.error(f"Document upload failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {str(e)}",
        )


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a document and all its chunks (admin only)."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admins can delete documents",
        )

    result = await db.execute(
        select(Document).where(Document.id == document_id)
    )
    doc = result.scalar_one_or_none()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    # Delete from vector store
    try:
        vector_store = VectorStore()
        vector_store.delete_document(document_id)
    except Exception as e:
        logger.warning(f"Vector store deletion warning: {e}")

    # Delete from PostgreSQL (cascades to chunks)
    doc.status = "deleted"

    return {
        "message": f"Document '{doc.title}' and {doc.chunk_count} chunks deleted",
    }
