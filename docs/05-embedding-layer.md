# 🧬 05 — Embedding Layer

> **Converting text into vector representations for semantic search**

---

## 🎯 Purpose

The Embedding Layer converts text chunks into **dense vector representations** (numerical arrays) that capture semantic meaning. These vectors enable similarity-based search — finding documents that are **semantically related**, not just keyword-matched.

---

## 🔍 How Embeddings Work

```
Input Text: "What is the refund policy?"
                    │
                    ▼
         ┌─────────────────┐
         │ Embedding Model  │
         │ (e.g. Ada-002)   │
         └────────┬────────┘
                  │
                  ▼
Output Vector: [0.0023, -0.0142, 0.0381, ..., 0.0089]
               ← — — — 1536 dimensions — — — →
```

**Key Insight:** Texts with similar meanings produce vectors that are close together in vector space.

```
"refund policy"        ──▶  [0.23, -0.14, 0.38, ...]  ┐
"return guidelines"    ──▶  [0.21, -0.12, 0.36, ...]  ├── Close (similar)
"money back process"   ──▶  [0.25, -0.11, 0.40, ...]  ┘

"engineering standup"  ──▶  [0.78, 0.52, -0.23, ...]  ← Far (different)
```

---

## 🛠 Embedding Model Options

| Model                      | Provider    | Dimensions | Speed     | Quality | Cost               |
| -------------------------- | ----------- | ---------- | --------- | ------- | ------------------ |
| **text-embedding-ada-002** | OpenAI      | 1536       | Fast      | High    | $0.0001/1K tokens  |
| **text-embedding-3-small** | OpenAI      | 1536       | Fast      | Higher  | $0.00002/1K tokens |
| **text-embedding-3-large** | OpenAI      | 3072       | Medium    | Highest | $0.00013/1K tokens |
| **all-MiniLM-L6-v2**       | HuggingFace | 384        | Very Fast | Good    | Free (self-hosted) |
| **all-mpnet-base-v2**      | HuggingFace | 768        | Fast      | Better  | Free (self-hosted) |

### Recommended for MVP: `text-embedding-3-small`

- Best price-performance ratio
- 1536 dimensions (good balance)
- High quality semantic understanding

---

## 💻 Implementation

```python
import openai
from typing import List
import numpy as np

class EmbeddingService:
    """Generate embeddings for text chunks using OpenAI."""

    def __init__(self, model: str = "text-embedding-3-small"):
        self.model = model
        self.client = openai.OpenAI()

    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        response = self.client.embeddings.create(
            input=text, model=self.model
        )
        return response.data[0].embedding

    def embed_batch(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """Generate embeddings for multiple texts in batches."""
        all_embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            response = self.client.embeddings.create(
                input=batch, model=self.model
            )
            embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(embeddings)
        return all_embeddings

    def embed_query(self, query: str) -> List[float]:
        """Embed a user query (same model for consistency)."""
        return self.embed_text(query)
```

### HuggingFace Alternative (Free, Self-Hosted)

```python
from sentence_transformers import SentenceTransformer

class LocalEmbeddingService:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> List[float]:
        return self.model.encode(text).tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts).tolist()
```

---

## 📐 Similarity Metrics

| Metric                 | Formula                    | Use Case                  |
| ---------------------- | -------------------------- | ------------------------- |
| **Cosine Similarity**  | cos(A,B) = A·B / (‖A‖·‖B‖) | Default — direction-based |
| **Euclidean Distance** | √Σ(Aᵢ-Bᵢ)²                 | Magnitude-sensitive       |
| **Dot Product**        | A·B = ΣAᵢ·Bᵢ               | Fastest computation       |

**We use Cosine Similarity** — it measures the angle between vectors, making it robust to vector magnitude differences.

---

## ⚡ Performance Tips

| Tip                  | Details                                                     |
| -------------------- | ----------------------------------------------------------- |
| **Batch Processing** | Embed 50-100 chunks per API call                            |
| **Caching**          | Cache embeddings — don't re-embed unchanged chunks          |
| **Rate Limiting**    | OpenAI allows 3,000 RPM — implement exponential backoff     |
| **Dimensionality**   | 1536 dims is optimal; 3072 only for highest precision needs |

---

_← [Text Processing](./04-text-processing.md) | [Vector Storage →](./06-vector-storage.md)_
