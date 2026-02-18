"""
Test Query Pipeline
====================
Unit tests for the RAG query orchestrator.
Uses mocks for external services (OpenAI, ChromaDB).
"""

import pytest
from unittest.mock import MagicMock, AsyncMock, patch

try:
    from app.services.query_pipeline import QueryPipeline
    from tests.fixtures import MOCK_CHROMA_RESULTS, MOCK_EMPTY_RESULTS
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False

skipif_no_deps = pytest.mark.skipif(
    not HAS_DEPS,
    reason="Skipping: missing dependency"
)


@skipif_no_deps
class TestQueryPipeline:
    """Test the RAG query pipeline orchestration."""

    def setup_method(self):
        """Set up mocked services for each test."""
        self.mock_embedder = MagicMock()
        self.mock_embedder.embed_query = MagicMock(return_value=[0.1] * 1536)

        self.mock_store = MagicMock()
        self.mock_store.search = MagicMock(return_value=MOCK_CHROMA_RESULTS)

        self.mock_llm = MagicMock()
        self.mock_llm.model = "gpt-4"
        self.mock_llm.generate = AsyncMock(return_value={
            "answer": "The refund policy allows returns within 30 days. [Source 1]",
            "tokens_used": {"prompt": 500, "completion": 100, "total": 600},
            "model": "gpt-4",
        })

        self.mock_rbac = MagicMock()
        self.mock_rbac.filter_chroma_results = MagicMock(
            return_value=MOCK_CHROMA_RESULTS
        )

        self.mock_cache = MagicMock()
        self.mock_cache.get = MagicMock(return_value=None)  # No cache hits
        self.mock_cache.set = MagicMock()

        self.pipeline = QueryPipeline(
            embedding_service=self.mock_embedder,
            vector_store=self.mock_store,
            llm_generator=self.mock_llm,
            rbac_service=self.mock_rbac,
            query_cache=self.mock_cache,
        )

    @pytest.mark.asyncio
    async def test_full_pipeline_returns_answer(self):
        """Test that the full pipeline produces a complete result."""
        result = await self.pipeline.process(
            question="What is the refund policy?",
            user_id="user-001",
            user_role="general",
        )

        assert "answer" in result
        assert "sources" in result
        assert "query_id" in result
        assert "confidence" in result
        assert "response_time_ms" in result
        assert result["answer"] != ""

    @pytest.mark.asyncio
    async def test_pipeline_calls_services_in_order(self):
        """Verify the pipeline calls services: embed → search → RBAC → generate."""
        await self.pipeline.process(
            question="test question",
            user_id="user-001",
            user_role="admin",
        )

        # Verify call order
        self.mock_embedder.embed_query.assert_called_once()
        self.mock_store.search.assert_called_once()
        self.mock_rbac.filter_chroma_results.assert_called_once()
        self.mock_llm.generate.assert_called_once()

    @pytest.mark.asyncio
    async def test_no_context_returns_fallback_message(self):
        """When no documents match, return a graceful fallback."""
        self.mock_store.search.return_value = MOCK_EMPTY_RESULTS
        self.mock_rbac.filter_chroma_results.return_value = MOCK_EMPTY_RESULTS

        result = await self.pipeline.process(
            question="Something completely unknown",
            user_id="user-001",
            user_role="general",
        )

        assert "don't have enough information" in result["answer"]
        self.mock_llm.generate.assert_not_called()

    @pytest.mark.asyncio
    async def test_confidence_assessment(self):
        """Test confidence scoring based on similarity scores."""
        result = await self.pipeline.process(
            question="What is the refund policy?",
            user_id="user-001",
            user_role="general",
        )

        assert result["confidence"] in ["high", "medium", "low"]

    @pytest.mark.asyncio
    async def test_sources_include_metadata(self):
        """Verify source citations include title, source, and document_id."""
        result = await self.pipeline.process(
            question="What is the refund policy?",
            user_id="user-001",
            user_role="general",
        )

        assert len(result["sources"]) > 0
        source = result["sources"][0]
        assert "title" in source
        assert "source" in source
        assert "document_id" in source
        assert "similarity_score" in source

    @pytest.mark.asyncio
    async def test_rbac_filters_applied(self):
        """Verify RBAC filtering is applied to search results."""
        await self.pipeline.process(
            question="test",
            user_id="user-001",
            user_role="engineering",
        )

        # RBAC filter was called with the search results
        self.mock_rbac.filter_chroma_results.assert_called_once_with(
            MOCK_CHROMA_RESULTS,
            "engineering",
        )

    def test_preprocess_strips_whitespace(self):
        """Test query preprocessing."""
        assert self.pipeline._preprocess("  hello world  ") == "hello world"

    def test_assess_confidence_levels(self):
        """Test confidence level thresholds."""
        assert self.pipeline._assess_confidence(0.90, 3) == "high"
        assert self.pipeline._assess_confidence(0.75, 1) == "medium"
        assert self.pipeline._assess_confidence(0.50, 1) == "low"
