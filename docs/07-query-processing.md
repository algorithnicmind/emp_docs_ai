# 🔍 07 — Query Processing Layer

> **From user question to relevant context retrieval**

---

## 🎯 Purpose

When a user asks a question, the Query Processing Layer:

1. Converts the question into a vector
2. Searches the vector DB for similar chunks
3. Applies access-level filtering (RBAC)
4. Assembles the most relevant context for the LLM

---

## 🔄 Query Pipeline

```
User: "What is the refund policy for enterprise customers?"
    │
    ▼
Step 1: QUERY PREPROCESSING
    │   • Clean and normalize
    │   • Detect language, intent
    │
    ▼
Step 2: QUERY EMBEDDING
    │   • Same model as indexing (text-embedding-3-small)
    │   • Output: 1536-dim vector
    │
    ▼
Step 3: SIMILARITY SEARCH
    │   • Search vector DB for Top-K (K=5)
    │   • Returns ranked chunks with similarity scores
    │
    ▼
Step 4: ACCESS FILTERING (RBAC)
    │   • Check user role vs chunk access_level
    │   • Remove unauthorized chunks
    │
    ▼
Step 5: RE-RANKING (Optional)
    │   • Cross-encoder re-ranking for precision
    │   • Score relevance more carefully
    │
    ▼
Step 6: CONTEXT ASSEMBLY
    │   • Combine Top-K chunks
    │   • Add source metadata for citations
    │   • Respect LLM context window
    │
    ▼
    OUTPUT: Structured context → LLM Generation Layer
```

---

## 💻 Implementation

```python
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class QueryResult:
    chunk_text: str
    document_id: str
    title: str
    source: str
    similarity_score: float
    department: str

class QueryProcessor:
    """Process user queries and retrieve relevant context."""

    def __init__(self, embedding_service, vector_store, rbac_service):
        self.embedder = embedding_service
        self.store = vector_store
        self.rbac = rbac_service

    async def process_query(
        self, question: str, user_id: str, top_k: int = 5
    ) -> List[QueryResult]:
        # Step 1: Preprocess
        cleaned_query = self._preprocess(question)

        # Step 2: Embed query
        query_vector = self.embedder.embed_query(cleaned_query)

        # Step 3: Similarity search
        raw_results = self.store.search(query_vector, top_k=top_k * 2)

        # Step 4: RBAC filter
        user_role = await self.rbac.get_user_role(user_id)
        filtered = self._apply_access_filter(raw_results, user_role)

        # Step 5: Take top K after filtering
        top_results = filtered[:top_k]

        # Step 6: Format results
        return [
            QueryResult(
                chunk_text=r["documents"][0],
                document_id=r["metadatas"][0]["document_id"],
                title=r["metadatas"][0]["title"],
                source=r["metadatas"][0]["source"],
                similarity_score=1 - r["distances"][0],
                department=r["metadatas"][0]["department"],
            )
            for r in self._unpack_results(top_results)
        ]

    def _preprocess(self, query: str) -> str:
        return query.strip().lower()

    def _apply_access_filter(self, results, user_role):
        """Filter results based on user's access permissions."""
        allowed = []
        for result in results:
            access = result.get("access_level", "all")
            if access == "all":
                allowed.append(result)
            elif access == "department" and self.rbac.has_dept_access(
                user_role, result["department"]
            ):
                allowed.append(result)
            elif access == "confidential" and user_role in ["admin", "hr"]:
                allowed.append(result)
        return allowed

    def assemble_context(self, results: List[QueryResult]) -> str:
        """Combine results into structured context for LLM."""
        context_parts = []
        for i, r in enumerate(results, 1):
            context_parts.append(
                f"[Source {i}: {r.title} ({r.source})]\n{r.chunk_text}\n"
            )
        return "\n---\n".join(context_parts)
```

---

## ⚙️ Configuration

| Parameter              | Default | Description                         |
| ---------------------- | ------- | ----------------------------------- |
| `top_k`                | 5       | Number of results to return         |
| `similarity_threshold` | 0.7     | Minimum similarity score            |
| `max_context_tokens`   | 3000    | Max tokens sent to LLM              |
| `search_expand_factor` | 2x      | Fetch 2x results before RBAC filter |

---

## 📊 Query Logging

Every query is logged for analytics:

```python
query_log = {
    "user_id": user_id,
    "question": question,
    "results_count": len(results),
    "top_score": results[0].similarity_score if results else 0,
    "response_time_ms": elapsed_ms,
    "timestamp": datetime.utcnow(),
}
```

---

_← [Vector Storage](./06-vector-storage.md) | [LLM Generation →](./08-llm-generation.md)_
