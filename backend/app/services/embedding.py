"""
Embedding Service
==================
Generate vector embeddings for text chunks using OpenAI.
Supports both single and batch embedding with rate-limiting.
"""

from typing import List

import openai
from loguru import logger

from app.config import get_settings

settings = get_settings()


class EmbeddingService:
    """Generate embeddings for text chunks using OpenAI API."""

    def __init__(
        self,
        model: str = None,
        api_key: str = None,
    ):
        self.model = model or settings.EMBEDDING_MODEL
        self.client = openai.OpenAI(
            api_key=api_key or settings.OPENAI_API_KEY
        )

    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text string.

        Args:
            text: The text to embed.

        Returns:
            A list of floats representing the embedding vector.
        """
        try:
            response = self.client.embeddings.create(
                input=text,
                model=self.model,
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Embedding failed for text (len={len(text)}): {e}")
            raise

    def embed_batch(
        self, texts: List[str], batch_size: int = 100
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batches.
        OpenAI supports up to ~2048 items per batch.

        Args:
            texts: List of text strings to embed.
            batch_size: Number of texts per API call (default 100).

        Returns:
            List of embedding vectors.
        """
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            try:
                response = self.client.embeddings.create(
                    input=batch,
                    model=self.model,
                )
                embeddings = [item.embedding for item in response.data]
                all_embeddings.extend(embeddings)

                logger.debug(
                    f"Embedded batch {i // batch_size + 1}: "
                    f"{len(batch)} texts"
                )
            except Exception as e:
                logger.error(
                    f"Batch embedding failed at index {i}: {e}"
                )
                raise

        logger.info(f"Generated {len(all_embeddings)} embeddings total")
        return all_embeddings

    def embed_query(self, query: str) -> List[float]:
        """
        Embed a user query using the same model used for document chunks.
        This ensures consistency between query and document vectors.

        Args:
            query: The user's natural language question.

        Returns:
            Embedding vector for the query.
        """
        return self.embed_text(query)
