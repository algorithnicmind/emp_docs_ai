"""
Query Pipeline — RAG Orchestrator
===================================
Orchestrates the complete Retrieval-Augmented Generation flow:
1. Preprocess query
2. Embed query
3. Search vector store
4. Apply RBAC filtering
5. Assemble context
6. Generate LLM response
7. Log query for analytics
"""

import time
import uuid
from typing import List, Optional, AsyncGenerator
from dataclasses import dataclass

from loguru import logger

from app.services.embedding import EmbeddingService
from app.services.retrieval import VectorStore
from app.services.generation import LLMGenerator
from app.services.rbac import RBACService
from app.config import get_settings

settings = get_settings()


@dataclass
class QueryResult:
    """Structured result from a single retrieved chunk."""
    chunk_text: str
    document_id: str
    title: str
    source: str
    similarity_score: float
    department: str


class QueryPipeline:
    """
    Orchestrates the complete RAG query pipeline.
    This is the main entry point for processing user questions.
    """

    def __init__(
        self,
        embedding_service: EmbeddingService = None,
        vector_store: VectorStore = None,
        llm_generator: LLMGenerator = None,
        rbac_service: RBACService = None,
    ):
        self.embedder = embedding_service or EmbeddingService()
        self.store = vector_store or VectorStore()
        self.llm = llm_generator or LLMGenerator()
        self.rbac = rbac_service or RBACService()

    async def process(
        self,
        question: str,
        user_id: str,
        user_role: str = "general",
        top_k: int = None,
    ) -> dict:
        """
        Full RAG pipeline: query → embed → search → filter → generate.

        Args:
            question: The user's natural language question.
            user_id: The user's ID for logging.
            user_role: The user's role for RBAC filtering.
            top_k: Number of results to retrieve.

        Returns:
            Dict with answer, sources, query_id, confidence, timing.
        """
        start_time = time.time()
        top_k = top_k or settings.TOP_K_RESULTS
        query_id = str(uuid.uuid4())

        logger.info(f"Processing query: '{question}' (user={user_id}, role={user_role})")

        # Step 1: Preprocess the query
        cleaned_query = self._preprocess(question)

        # Step 2: Embed the query
        query_vector = self.embedder.embed_query(cleaned_query)

        # Step 3: Similarity search (fetch 2x for RBAC filtering)
        raw_results = self.store.search(query_vector, top_k=top_k * 2)

        # Step 4: RBAC filter
        filtered_results = self.rbac.filter_chroma_results(raw_results, user_role)

        # Step 5: Prepare context and sources
        context, sources = self._assemble_context(filtered_results, top_k)

        # Step 6: Generate answer
        if not context.strip():
            answer_text = (
                "I don't have enough information in the available documents "
                "to answer this question. Please try rephrasing or contact "
                "your team lead for assistance."
            )
            tokens_used = {"prompt": 0, "completion": 0, "total": 0}
            model_used = self.llm.model
        else:
            llm_result = await self.llm.generate(context, question)
            answer_text = llm_result["answer"]
            tokens_used = llm_result["tokens_used"]
            model_used = llm_result["model"]

        elapsed_ms = int((time.time() - start_time) * 1000)

        # Determine confidence level
        top_score = self._get_top_score(filtered_results)
        confidence = self._assess_confidence(top_score, len(sources))

        result = {
            "query_id": query_id,
            "answer": answer_text,
            "sources": sources,
            "confidence": confidence,
            "response_time_ms": elapsed_ms,
            "model": model_used,
            "tokens_used": tokens_used,
            "top_similarity_score": top_score,
        }

        logger.info(
            f"Query completed: {elapsed_ms}ms, "
            f"{len(sources)} sources, "
            f"confidence={confidence}"
        )

        return result

    async def process_stream(
        self,
        question: str,
        user_id: str,
        user_role: str = "general",
        top_k: int = None,
    ) -> AsyncGenerator[str, None]:
        """
        Streaming RAG pipeline — yields tokens as they are generated.
        """
        top_k = top_k or settings.TOP_K_RESULTS
        cleaned_query = self._preprocess(question)
        query_vector = self.embedder.embed_query(cleaned_query)
        raw_results = self.store.search(query_vector, top_k=top_k * 2)
        filtered_results = self.rbac.filter_chroma_results(raw_results, user_role)
        context, sources = self._assemble_context(filtered_results, top_k)

        if not context.strip():
            yield "I don't have enough information to answer this question."
            return

        async for token in self.llm.generate_stream(context, question):
            yield token

    def _preprocess(self, query: str) -> str:
        """Clean and normalize the query."""
        return query.strip()

    def _assemble_context(self, results: dict, top_k: int) -> tuple:
        """
        Assemble context string and sources list from ChromaDB results.

        Returns:
            Tuple of (context_string, sources_list).
        """
        if not results["ids"][0]:
            return "", []

        context_parts = []
        sources = []

        for i in range(min(top_k, len(results["ids"][0]))):
            doc_text = results["documents"][0][i]
            metadata = results["metadatas"][0][i]
            distance = results["distances"][0][i]

            context_parts.append(
                f"[Source {i + 1}: {metadata['title']} ({metadata['source']})]\n"
                f"{doc_text}\n"
            )

            sources.append({
                "index": i + 1,
                "title": metadata["title"],
                "source": metadata["source"],
                "document_id": metadata["document_id"],
                "similarity_score": round(1 - distance, 4),
            })

        context = "\n---\n".join(context_parts)
        return context, sources

    def _get_top_score(self, results: dict) -> float:
        """Get the best similarity score from results."""
        if results["distances"][0]:
            return round(1 - results["distances"][0][0], 4)
        return 0.0

    def _assess_confidence(self, top_score: float, num_sources: int) -> str:
        """Determine confidence level based on similarity and source count."""
        if top_score >= 0.85 and num_sources >= 2:
            return "high"
        elif top_score >= 0.70:
            return "medium"
        else:
            return "low"
