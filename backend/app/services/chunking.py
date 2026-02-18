"""
Text Processing & Chunking Service
====================================
Cleans raw text and splits it into semantically meaningful chunks
with configurable overlap for embedding.
"""

import re
from typing import List

import tiktoken
from bs4 import BeautifulSoup
from loguru import logger

from app.config import get_settings

settings = get_settings()


class TextCleaner:
    """Clean and normalize raw document text."""

    def clean(self, text: str) -> str:
        """Remove HTML, normalize whitespace, strip boilerplate."""
        # Strip any residual HTML
        text = BeautifulSoup(text, "html.parser").get_text()

        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)

        # Fix encoding artifacts
        text = text.encode('utf-8', errors='ignore').decode('utf-8')

        # Collapse excessive newlines
        text = re.sub(r'\n{3,}', '\n\n', text)

        # Remove common boilerplate patterns
        text = self._remove_boilerplate(text)

        return text.strip()

    def _remove_boilerplate(self, text: str) -> str:
        """Remove common page headers/footers from extracted text."""
        patterns = [
            r'Page \d+ of \d+',
            r'©.*?\d{4}',
            r'CONFIDENTIAL',
            r'DRAFT',
        ]
        for pattern in patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        return text


class SemanticChunker:
    """
    Split documents into semantically meaningful chunks
    with configurable overlap.

    Respects section boundaries (paragraph breaks) to maintain
    semantic coherence within each chunk.
    """

    def __init__(
        self,
        chunk_size: int = None,
        overlap: int = None,
        min_chunk_size: int = 100,
    ):
        self.chunk_size = chunk_size or settings.CHUNK_SIZE
        self.overlap = overlap or settings.CHUNK_OVERLAP
        self.min_chunk_size = min_chunk_size
        self.tokenizer = tiktoken.encoding_for_model("gpt-4")

    def chunk_document(self, text: str, doc_id: str) -> List[dict]:
        """
        Split text into chunks respecting paragraph boundaries.

        Args:
            text: The cleaned document text.
            doc_id: Parent document ID for reference.

        Returns:
            List of chunk dictionaries ready for embedding.
        """
        # Split by double newlines (paragraphs / sections)
        sections = text.split("\n\n")
        chunks = []
        current = ""
        idx = 0

        for section in sections:
            section = section.strip()
            if not section:
                continue

            # If adding this section stays within chunk_size
            if self._count_tokens(current + " " + section) <= self.chunk_size:
                current = (current + "\n\n" + section).strip()
            else:
                # Save current chunk if it's big enough
                if current and self._count_tokens(current) >= self.min_chunk_size:
                    chunks.append(self._make_chunk(current, idx, doc_id))
                    idx += 1

                    # Get overlap from the end of the current chunk
                    overlap_text = self._get_overlap(current)
                    current = (overlap_text + "\n\n" + section).strip()
                else:
                    # Current chunk too small, just keep appending
                    current = (current + "\n\n" + section).strip()

        # Don't forget the last chunk
        if current.strip() and self._count_tokens(current) >= self.min_chunk_size:
            chunks.append(self._make_chunk(current.strip(), idx, doc_id))

        logger.info(
            f"Chunked document {doc_id}: {len(chunks)} chunks "
            f"(size={self.chunk_size}, overlap={self.overlap})"
        )

        return chunks

    def _count_tokens(self, text: str) -> int:
        """Count tokens using tiktoken."""
        return len(self.tokenizer.encode(text))

    def _get_overlap(self, text: str) -> str:
        """Get the last `overlap` tokens from text for continuity."""
        tokens = self.tokenizer.encode(text)
        overlap_tokens = tokens[-self.overlap:] if len(tokens) > self.overlap else tokens
        return self.tokenizer.decode(overlap_tokens)

    def _make_chunk(self, text: str, index: int, doc_id: str) -> dict:
        """Create a chunk dictionary."""
        return {
            "chunk_id": f"{doc_id}_chunk_{index:04d}",
            "document_id": doc_id,
            "chunk_text": text,
            "chunk_index": index,
            "token_count": self._count_tokens(text),
        }


# ── Convenience Functions ────────────────────────────────────

def process_text(raw_text: str, doc_id: str) -> List[dict]:
    """Clean text and split into chunks — one-step convenience function."""
    cleaner = TextCleaner()
    chunker = SemanticChunker()

    cleaned = cleaner.clean(raw_text)
    chunks = chunker.chunk_document(cleaned, doc_id)

    return chunks
