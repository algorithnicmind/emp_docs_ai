"""
Test Ingestion Service
=======================
Unit tests for the document ingestion pipeline.
"""

import os
import tempfile
import pytest

from app.services.ingestion import (
    MarkdownIngester,
    PlainTextIngester,
    get_ingester,
    UnifiedDocument,
)


class TestPlainTextIngester:
    """Test plain text file ingestion."""

    def test_ingests_text_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
            f.write("This is a test document.\nIt has multiple lines.\nThird line here.")
            f.flush()
            path = f.name

        try:
            ingester = PlainTextIngester()
            doc = ingester.ingest(path, {"title": "Test Doc"})

            assert isinstance(doc, UnifiedDocument)
            assert "test document" in doc.raw_text
            assert doc.metadata.title == "Test Doc"
            assert doc.metadata.file_type == "txt"
            assert doc.metadata.word_count > 0
        finally:
            os.unlink(path)

    def test_preserves_metadata(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
            f.write("Content here.")
            f.flush()
            path = f.name

        try:
            ingester = PlainTextIngester()
            doc = ingester.ingest(path, {
                "title": "HR Policy",
                "department": "hr",
                "access_level": "confidential",
            })

            assert doc.metadata.department == "hr"
            assert doc.metadata.access_level == "confidential"
        finally:
            os.unlink(path)


class TestMarkdownIngester:
    """Test Markdown file ingestion."""

    def test_strips_markdown_formatting(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write("# Heading\n\n**Bold text** and *italic text*.\n\n- Item 1\n- Item 2")
            f.flush()
            path = f.name

        try:
            ingester = MarkdownIngester()
            doc = ingester.ingest(path, {"title": "MD Doc"})

            assert isinstance(doc, UnifiedDocument)
            assert "Heading" in doc.raw_text
            assert "Bold text" in doc.raw_text
            assert "**" not in doc.raw_text  # Markdown syntax stripped
            assert doc.metadata.file_type == "md"
        finally:
            os.unlink(path)


class TestIngesterFactory:
    """Test the ingester factory function."""

    def test_pdf_by_content_type(self):
        ingester = get_ingester(content_type="application/pdf")
        assert ingester.__class__.__name__ == "PDFIngester"

    def test_markdown_by_extension(self):
        ingester = get_ingester(file_path="document.md")
        assert ingester.__class__.__name__ == "MarkdownIngester"

    def test_text_by_extension(self):
        ingester = get_ingester(file_path="notes.txt")
        assert ingester.__class__.__name__ == "PlainTextIngester"

    def test_unsupported_raises_error(self):
        with pytest.raises(ValueError, match="Unsupported file type"):
            get_ingester(content_type="image/png", file_path="photo.png")

    def test_extension_fallback(self):
        """When content_type is unknown, fallback to file extension."""
        ingester = get_ingester(content_type="application/octet-stream", file_path="doc.md")
        assert ingester.__class__.__name__ == "MarkdownIngester"
