"""
Vector Store Service
=====================
Manages vector storage using ChromaDB for similarity search.
Supports adding, searching, and deleting document embeddings.
"""

from typing import List, Optional

import chromadb
from loguru import logger

from app.config import get_settings

settings = get_settings()


class VectorStore:
    """
    Manages vector storage using ChromaDB.
    Provides persistent storage with metadata filtering.
    """

    def __init__(self, persist_dir: str = None, collection_name: str = "documents"):
        self.persist_dir = persist_dir or settings.VECTOR_STORE_PATH
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )
        logger.info(
            f"VectorStore initialized: {self.persist_dir} "
            f"(collection='{collection_name}', "
            f"count={self.collection.count()})"
        )

    def add_chunks(
        self,
        chunks: List[dict],
        embeddings: List[List[float]],
        doc_metadata: dict,
    ) -> int:
        """
        Store chunks with their embeddings and metadata.

        Args:
            chunks: List of chunk dictionaries.
            embeddings: Corresponding embedding vectors.
            doc_metadata: Document-level metadata to tag on each chunk.

        Returns:
            Number of chunks added.
        """
        ids = [c["chunk_id"] for c in chunks]
        documents = [c["chunk_text"] for c in chunks]
        metadatas = [
            {
                "document_id": c["document_id"],
                "chunk_index": c["chunk_index"],
                "department": doc_metadata.get("department", "general"),
                "access_level": doc_metadata.get("access_level", "all"),
                "title": doc_metadata.get("title", "Untitled"),
                "source": doc_metadata.get("source", "unknown"),
            }
            for c in chunks
        ]

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

        logger.info(f"Added {len(chunks)} chunks to vector store")
        return len(chunks)

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        filters: Optional[dict] = None,
    ) -> dict:
        """
        Search for similar chunks using cosine similarity.

        Args:
            query_embedding: The query vector.
            top_k: Number of results to return.
            filters: Optional ChromaDB where-filter for metadata.

        Returns:
            ChromaDB query results dict with documents, metadatas, distances.
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filters if filters else None,
            include=["documents", "metadatas", "distances"],
        )

        logger.debug(
            f"Vector search returned {len(results['ids'][0])} results "
            f"(top_k={top_k})"
        )

        return results

    def delete_document(self, document_id: str) -> None:
        """Delete all chunks belonging to a specific document."""
        self.collection.delete(where={"document_id": document_id})
        logger.info(f"Deleted all chunks for document {document_id}")

    def get_stats(self) -> dict:
        """Get collection statistics."""
        return {
            "total_chunks": self.collection.count(),
            "collection_name": self.collection.name,
            "persist_dir": self.persist_dir,
        }
