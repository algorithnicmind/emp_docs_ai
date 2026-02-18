# ⚡ 15 — Performance & Optimization

> **Caching, batching, streaming, and scalability strategies**

---

## 🎯 Performance Goals

| Metric                | Target        | Current |
| --------------------- | ------------- | ------- |
| Query response time   | < 5s          | TBD     |
| Document indexing     | < 30s per doc | TBD     |
| Concurrent users      | 100+          | TBD     |
| Vector search latency | < 50ms        | TBD     |
| Uptime                | 99.9%         | TBD     |

---

## 🗂️ Caching Strategy

### Query Cache (Redis)

Cache frequent questions to avoid redundant LLM calls:

```python
import redis
import hashlib
import json

class QueryCache:
    def __init__(self, redis_url: str, ttl: int = 3600):
        self.redis = redis.from_url(redis_url)
        self.ttl = ttl  # Cache for 1 hour

    def _key(self, question: str, user_role: str) -> str:
        raw = f"{question.lower().strip()}:{user_role}"
        return f"query:{hashlib.md5(raw.encode()).hexdigest()}"

    def get(self, question: str, user_role: str):
        key = self._key(question, user_role)
        cached = self.redis.get(key)
        return json.loads(cached) if cached else None

    def set(self, question: str, user_role: str, result: dict):
        key = self._key(question, user_role)
        self.redis.setex(key, self.ttl, json.dumps(result))

    def invalidate_all(self):
        """Clear cache when documents are re-indexed."""
        for key in self.redis.scan_iter("query:*"):
            self.redis.delete(key)
```

### Cache Invalidation

| Event                | Action                      |
| -------------------- | --------------------------- |
| New document indexed | Clear related queries       |
| Document deleted     | Invalidate all cache        |
| Document updated     | Clear related queries       |
| Scheduled            | Full invalidation every 24h |

---

## 📦 Batch Processing

### Embedding Batching

```python
async def batch_embed_and_store(chunks: list, batch_size: int = 50):
    """Process embeddings in batches to optimize API usage."""
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        texts = [c["chunk_text"] for c in batch]

        # Single API call for batch
        embeddings = embedding_service.embed_batch(texts)

        # Batch insert to vector store
        vector_store.add_chunks(batch, embeddings)

        # Rate limit protection
        await asyncio.sleep(0.5)
```

---

## 🌊 Streaming Responses

For Slack and Web, stream LLM responses for faster perceived performance:

```python
@router.post("/api/query/stream")
async def stream_query(request: QueryRequest, user = Depends(get_current_user)):
    context = await get_context(request.question, user)

    async def generate():
        async for token in llm.generate_stream(context, request.question):
            yield f"data: {json.dumps({'token': token})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
```

---

## 📐 Token Optimization

| Strategy            | Savings     | Implementation                   |
| ------------------- | ----------- | -------------------------------- |
| **Limit context**   | ~40% tokens | Max 3000 tokens of context       |
| **Shorter prompts** | ~10% tokens | Concise system instructions      |
| **Cache results**   | 100% (hits) | Redis query cache                |
| **Smaller model**   | ~50% cost   | GPT-3.5-turbo for simple queries |

---

## 🔄 Async Processing

```python
from celery import Celery

celery_app = Celery("worker", broker="redis://localhost:6379")

@celery_app.task
def process_document_async(document_id: str):
    """Background task for document processing."""
    document = Document.get(document_id)
    chunks = chunker.chunk_document(document.raw_text, document.id)
    embeddings = embedding_service.embed_batch([c["chunk_text"] for c in chunks])
    vector_store.add_chunks(chunks, embeddings)
    document.status = "indexed"
    document.save()
```

---

## 📊 Scalability Tiers

| Tier           | Users  | Infrastructure         | Vector DB | Response Time |
| -------------- | ------ | ---------------------- | --------- | ------------- |
| **MVP**        | 1-50   | Single server          | FAISS     | < 5s          |
| **Growth**     | 50-500 | Docker Compose + Redis | ChromaDB  | < 3s          |
| **Enterprise** | 500+   | Kubernetes             | Pinecone  | < 2s          |

---

## 📈 Monitoring

| Tool                 | Purpose                 |
| -------------------- | ----------------------- |
| **Prometheus**       | Metrics collection      |
| **Grafana**          | Dashboard visualization |
| **Sentry**           | Error tracking          |
| **Application logs** | Structured JSON logging |

---

_← [Security](./14-security.md) | [Deployment Guide →](./16-deployment.md)_
