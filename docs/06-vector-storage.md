# 🗄️ 06 — Vector Storage Layer

> **Storing and indexing embeddings for fast retrieval**

---

## 🎯 Purpose

The Vector Storage Layer stores embedding vectors and their metadata, enabling **fast similarity search** across potentially millions of document chunks.

---

## 🔧 Vector DB Options

| Database     | Type              | Best For           | Scalability    | Cost      |
| ------------ | ----------------- | ------------------ | -------------- | --------- |
| **FAISS**    | Local library     | Hackathon / MVP    | Single machine | Free      |
| **ChromaDB** | Embedded DB       | Small-medium teams | Moderate       | Free      |
| **Pinecone** | Managed cloud     | Enterprise         | Unlimited      | Paid      |
| **Weaviate** | Self-hosted/cloud | Advanced use cases | High           | Free/Paid |
| **Qdrant**   | Self-hosted/cloud | High performance   | High           | Free/Paid |

### Recommended for MVP: **ChromaDB**

- Easy setup, Python-native
- Built-in metadata filtering
- Persistent storage
- No infrastructure needed

---

## 💻 ChromaDB Implementation

```python
import chromadb
from chromadb.config import Settings

class VectorStore:
    """Manage vector storage using ChromaDB."""

    def __init__(self, persist_dir: str = "./vector_store"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )

    def add_chunks(self, chunks: list, embeddings: list):
        """Store chunks with their embeddings."""
        self.collection.add(
            ids=[c["chunk_id"] for c in chunks],
            embeddings=embeddings,
            documents=[c["chunk_text"] for c in chunks],
            metadatas=[{
                "document_id": c["document_id"],
                "department": c["metadata"]["department"],
                "access_level": c["metadata"]["access_level"],
                "title": c["metadata"]["title"],
                "source": c["metadata"]["source"],
            } for c in chunks]
        )

    def search(self, query_embedding: list, top_k: int = 5,
               filters: dict = None) -> dict:
        """Search for similar chunks."""
        where_filter = filters if filters else None
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_filter,
            include=["documents", "metadatas", "distances"]
        )
        return results

    def delete_document(self, document_id: str):
        """Delete all chunks for a document."""
        self.collection.delete(where={"document_id": document_id})

    def get_stats(self) -> dict:
        """Get collection statistics."""
        return {"total_chunks": self.collection.count()}
```

---

## 🗄️ FAISS Alternative

```python
import faiss
import numpy as np
import pickle

class FAISSVectorStore:
    def __init__(self, dimension: int = 1536):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)  # Inner product (cosine)
        self.metadata_store = {}
        self.id_map = []

    def add(self, embeddings: list, chunks: list):
        vectors = np.array(embeddings).astype('float32')
        faiss.normalize_L2(vectors)  # Normalize for cosine similarity
        start_id = len(self.id_map)
        self.index.add(vectors)
        for i, chunk in enumerate(chunks):
            self.id_map.append(chunk["chunk_id"])
            self.metadata_store[chunk["chunk_id"]] = chunk

    def search(self, query_embedding: list, top_k: int = 5):
        query = np.array([query_embedding]).astype('float32')
        faiss.normalize_L2(query)
        scores, indices = self.index.search(query, top_k)
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.id_map):
                chunk_id = self.id_map[idx]
                results.append({
                    "chunk": self.metadata_store[chunk_id],
                    "score": float(score)
                })
        return results
```

---

## 📊 Stored Fields

| Field          | Type    | Description                  |
| -------------- | ------- | ---------------------------- |
| `vector`       | float[] | Embedding vector (1536 dims) |
| `chunk_id`     | string  | Unique chunk identifier      |
| `chunk_text`   | string  | Original text content        |
| `document_id`  | string  | Parent document ID           |
| `department`   | string  | Owning department            |
| `access_level` | string  | Permission level             |
| `title`        | string  | Document title               |
| `source`       | string  | Origin source type           |

---

## ⚡ Indexing Performance

| Operation        | FAISS (Local) | ChromaDB | Pinecone  |
| ---------------- | :-----------: | :------: | :-------: |
| Insert 1K chunks |     ~0.5s     |   ~1s    |    ~2s    |
| Search (Top 5)   |     ~1ms      |   ~5ms   |   ~50ms   |
| Max vectors      |     ~10M      |   ~1M    | Unlimited |

---

_← [Embedding Layer](./05-embedding-layer.md) | [Query Processing →](./07-query-processing.md)_
