"""
Test Chunking Service
======================
Unit tests for the text cleaning and chunking logic.
"""

import pytest
from app.services.chunking import TextCleaner, SemanticChunker


class TestTextCleaner:
    """Test the text cleaning functionality."""

    def setup_method(self):
        self.cleaner = TextCleaner()

    def test_removes_html_tags(self):
        text = "<p>Hello <b>World</b></p>"
        cleaned = self.cleaner.clean(text)
        assert "<p>" not in cleaned
        assert "<b>" not in cleaned
        assert "Hello" in cleaned
        assert "World" in cleaned

    def test_normalizes_whitespace(self):
        text = "Hello    World   Test"
        cleaned = self.cleaner.clean(text)
        assert "    " not in cleaned

    def test_removes_page_numbers(self):
        text = "Content here Page 1 of 5 more content"
        cleaned = self.cleaner.clean(text)
        assert "Page 1 of 5" not in cleaned

    def test_handles_empty_string(self):
        assert self.cleaner.clean("") == ""


class TestSemanticChunker:
    """Test the semantic chunking functionality."""

    def setup_method(self):
        self.chunker = SemanticChunker(chunk_size=100, overlap=20, min_chunk_size=10)

    def test_creates_chunks(self):
        text = "First paragraph with detailed content about the company policies and procedures.\n\nSecond paragraph discussing employee benefits and onboarding processes.\n\nThird paragraph explaining the Q&A system architecture and design."
        chunks = self.chunker.chunk_document(text, "test_doc")
        assert len(chunks) >= 1

    def test_chunk_has_required_fields(self):
        text = "This is a test document with enough content to create a chunk. It contains multiple sentences about various topics and is long enough to pass the minimum chunk size threshold easily."
        chunks = self.chunker.chunk_document(text, "doc_001")
        assert len(chunks) >= 1

        chunk = chunks[0]
        assert "chunk_id" in chunk
        assert "document_id" in chunk
        assert "chunk_text" in chunk
        assert "chunk_index" in chunk
        assert "token_count" in chunk

    def test_chunk_id_format(self):
        text = "Test content for chunking with enough words so that the chunker can produce at least one chunk above the minimum size threshold of ten tokens."
        chunks = self.chunker.chunk_document(text, "doc_123")
        assert chunks[0]["chunk_id"].startswith("doc_123_chunk_")

    def test_chunk_index_sequential(self):
        text = "\n\n".join([f"Paragraph {i} with some content." for i in range(20)])
        chunks = self.chunker.chunk_document(text, "doc_001")
        for i, chunk in enumerate(chunks):
            assert chunk["chunk_index"] == i
