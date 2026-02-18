"""
Query Cache Service (Redis)
============================
Caches frequent queries to avoid redundant LLM calls.
Cache is keyed by (question + user_role) to respect RBAC.
"""

import hashlib
import json
from typing import Optional

from loguru import logger
from app.config import get_settings

settings = get_settings()


class QueryCache:
    """
    Redis-backed query cache.

    Cache key format: query:{md5(question:role)}
    TTL: 1 hour by default (configurable).
    """

    def __init__(self, redis_url: str = None, ttl: int = 3600):
        self.ttl = ttl
        self._redis = None
        self._redis_url = redis_url or settings.REDIS_URL

    def _get_client(self):
        """Lazy-initialize Redis connection."""
        if self._redis is None:
            try:
                import redis
                self._redis = redis.from_url(
                    self._redis_url,
                    decode_responses=True,
                    socket_connect_timeout=2,
                )
                self._redis.ping()
                logger.info("✅ Redis cache connected")
            except Exception as e:
                logger.warning(f"⚠️ Redis unavailable, caching disabled: {e}")
                self._redis = None
        return self._redis

    def _make_key(self, question: str, user_role: str) -> str:
        """Generate a cache key from question + role."""
        raw = f"{question.lower().strip()}:{user_role}"
        digest = hashlib.md5(raw.encode()).hexdigest()
        return f"query:{digest}"

    def get(self, question: str, user_role: str) -> Optional[dict]:
        """
        Retrieve a cached query result.

        Returns:
            Cached result dict, or None if not found.
        """
        client = self._get_client()
        if not client:
            return None

        try:
            key = self._make_key(question, user_role)
            cached = client.get(key)
            if cached:
                logger.debug(f"Cache HIT for: '{question[:50]}...'")
                return json.loads(cached)
            logger.debug(f"Cache MISS for: '{question[:50]}...'")
            return None
        except Exception as e:
            logger.warning(f"Cache get failed: {e}")
            return None

    def set(self, question: str, user_role: str, result: dict) -> None:
        """
        Cache a query result with TTL.

        Args:
            question: The original question.
            user_role: The user's role (for RBAC-aware caching).
            result: The query pipeline result to cache.
        """
        client = self._get_client()
        if not client:
            return

        try:
            key = self._make_key(question, user_role)
            # Make result JSON-serializable
            serializable = {
                "query_id": result.get("query_id"),
                "answer": result.get("answer"),
                "sources": result.get("sources", []),
                "confidence": result.get("confidence"),
                "response_time_ms": result.get("response_time_ms"),
                "cached": True,
            }
            client.setex(key, self.ttl, json.dumps(serializable))
            logger.debug(f"Cached result for: '{question[:50]}...'")
        except Exception as e:
            logger.warning(f"Cache set failed: {e}")

    def invalidate_all(self) -> int:
        """
        Clear all query cache entries.
        Called when documents are re-indexed or deleted.

        Returns:
            Number of keys deleted.
        """
        client = self._get_client()
        if not client:
            return 0

        try:
            keys = list(client.scan_iter("query:*"))
            if keys:
                deleted = client.delete(*keys)
                logger.info(f"🗑️ Invalidated {deleted} cached queries")
                return deleted
            return 0
        except Exception as e:
            logger.warning(f"Cache invalidation failed: {e}")
            return 0

    def is_available(self) -> bool:
        """Check if Redis is connected."""
        client = self._get_client()
        if not client:
            return False
        try:
            client.ping()
            return True
        except Exception:
            return False
