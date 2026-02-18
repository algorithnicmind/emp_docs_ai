"""
Document Ingestion Service
===========================
Handles ingesting documents from multiple sources:
- PDF files (pdfplumber)
- Markdown files
- Plain text files

Normalizes all documents into a UnifiedDocument format.
"""

from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, List

import pdfplumber
import markdown
from bs4 import BeautifulSoup
from loguru import logger


# ── Unified Document Schema ──────────────────────────────────

@dataclass
class DocumentMetadata:
    """Standardized metadata for any ingested document."""
    title: str
    author: str = "Unknown"
    department: str = "general"
    access_level: str = "all"
    source: str = "pdf_upload"
    source_url: Optional[str] = None
    file_type: str = "pdf"
    page_count: Optional[int] = None
    word_count: int = 0
    tags: List[str] = field(default_factory=list)
    uploaded_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )


@dataclass
class UnifiedDocument:
    """Standardized document representation after ingestion."""
    raw_text: str
    metadata: DocumentMetadata


# ── Ingesters ────────────────────────────────────────────────

class PDFIngester:
    """Extract text and metadata from PDF files using pdfplumber."""

    def ingest(self, file_path: str, metadata: dict) -> UnifiedDocument:
        path = Path(file_path)
        text = ""
        page_count = 0

        try:
            with pdfplumber.open(file_path) as pdf:
                page_count = len(pdf.pages)
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            logger.error(f"PDF parsing failed for {file_path}: {e}")
            raise

        word_count = len(text.split())

        doc_metadata = DocumentMetadata(
            title=metadata.get("title", path.stem),
            author=metadata.get("author", "Unknown"),
            department=metadata.get("department", "general"),
            access_level=metadata.get("access_level", "all"),
            source="pdf_upload",
            file_type="pdf",
            page_count=page_count,
            word_count=word_count,
        )

        logger.info(
            f"Ingested PDF: '{doc_metadata.title}' "
            f"({page_count} pages, {word_count} words)"
        )

        return UnifiedDocument(raw_text=text, metadata=doc_metadata)


class MarkdownIngester:
    """Extract text from Markdown files, stripping formatting."""

    def ingest(self, file_path: str, metadata: dict) -> UnifiedDocument:
        path = Path(file_path)

        with open(file_path, "r", encoding="utf-8") as f:
            md_content = f.read()

        # Convert MD → HTML → plain text
        html = markdown.markdown(md_content)
        text = BeautifulSoup(html, "html.parser").get_text(separator="\n")
        word_count = len(text.split())

        doc_metadata = DocumentMetadata(
            title=metadata.get("title", path.stem),
            author=metadata.get("author", "Unknown"),
            department=metadata.get("department", "general"),
            access_level=metadata.get("access_level", "all"),
            source="markdown",
            file_type="md",
            word_count=word_count,
        )

        logger.info(
            f"Ingested Markdown: '{doc_metadata.title}' ({word_count} words)"
        )

        return UnifiedDocument(raw_text=text, metadata=doc_metadata)


class PlainTextIngester:
    """Extract text from plain .txt files."""

    def ingest(self, file_path: str, metadata: dict) -> UnifiedDocument:
        path = Path(file_path)

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        word_count = len(text.split())

        doc_metadata = DocumentMetadata(
            title=metadata.get("title", path.stem),
            author=metadata.get("author", "Unknown"),
            department=metadata.get("department", "general"),
            access_level=metadata.get("access_level", "all"),
            source="plain_text",
            file_type="txt",
            word_count=word_count,
        )

        logger.info(
            f"Ingested Text: '{doc_metadata.title}' ({word_count} words)"
        )

        return UnifiedDocument(raw_text=text, metadata=doc_metadata)


# ── Ingester Factory ─────────────────────────────────────────

INGESTER_MAP = {
    "application/pdf": PDFIngester,
    "text/markdown": MarkdownIngester,
    "text/plain": PlainTextIngester,
    # File extension fallbacks
    ".pdf": PDFIngester,
    ".md": MarkdownIngester,
    ".txt": PlainTextIngester,
}


def get_ingester(content_type: str = None, file_path: str = None):
    """
    Get the appropriate ingester based on content type or file extension.
    """
    if content_type and content_type in INGESTER_MAP:
        return INGESTER_MAP[content_type]()

    if file_path:
        ext = Path(file_path).suffix.lower()
        if ext in INGESTER_MAP:
            return INGESTER_MAP[ext]()

    raise ValueError(
        f"Unsupported file type: content_type={content_type}, file_path={file_path}"
    )
