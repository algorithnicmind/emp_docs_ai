# ✂️ 04 — Text Processing & Chunking

> **Breaking documents into semantically meaningful pieces**

---

## 🎯 Purpose

Large documents cannot be directly embedded effectively due to:

- **Token limits** — Embedding models have maximum input lengths
- **Diluted semantics** — Long texts produce averaged, less meaningful vectors
- **Retrieval precision** — Smaller chunks enable more precise search results

---

## 🔄 Processing Pipeline

```
RAW DOCUMENT TEXT
      │
      ▼
┌─────────────────────┐
│  1. TEXT CLEANING    │  Remove HTML, normalize whitespace, fix encoding
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  2. SECTION DETECT   │  Identify headings, paragraphs, lists, tables
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  3. CHUNKING         │  Split into 500–1000 token chunks with overlap
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  4. METADATA TAG     │  Assign chunk_id, link to doc_id, position info
└──────────┬──────────┘
           ▼
     PROCESSED CHUNKS → Ready for Embedding
```

---

## 🧹 Text Cleaning

```python
import re
from bs4 import BeautifulSoup

class TextCleaner:
    def clean(self, text: str) -> str:
        text = BeautifulSoup(text, "html.parser").get_text()
        text = re.sub(r'\s+', ' ', text)
        text = text.encode('utf-8', errors='ignore').decode('utf-8')
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = self._remove_boilerplate(text)
        return text.strip()

    def _remove_boilerplate(self, text: str) -> str:
        patterns = [r'Page \d+ of \d+', r'©.*?\d{4}']
        for pattern in patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        return text
```

---

## ✂️ Chunking Strategy

### Why Overlap?

```
WITHOUT OVERLAP:  "...refund is available" | "within 30 days"  ← Split!
WITH OVERLAP:     "...refund is available within 30 days" (shared)
```

### Configuration

| Parameter        | Default     | Range    | Description            |
| ---------------- | ----------- | -------- | ---------------------- |
| `chunk_size`     | 800 tokens  | 500–1000 | Target chunk size      |
| `chunk_overlap`  | 100 tokens  | 50–200   | Overlap between chunks |
| `min_chunk_size` | 100 tokens  | 50–200   | Minimum viable chunk   |
| `max_chunk_size` | 1000 tokens | 800–2000 | Hard maximum           |

### Algorithm

```python
from typing import List
import tiktoken

class SemanticChunker:
    def __init__(self, chunk_size=800, overlap=100):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.tokenizer = tiktoken.encoding_for_model("gpt-4")

    def chunk_document(self, text: str, doc_id: str) -> List[dict]:
        sections = text.split("\n\n")
        chunks, current, idx = [], "", 0

        for section in sections:
            if self._tokens(current + section) <= self.chunk_size:
                current += section + "\n\n"
            else:
                if current:
                    chunks.append(self._make_chunk(current.strip(), idx, doc_id))
                    idx += 1
                    overlap_text = self._get_overlap(current)
                    current = overlap_text + section + "\n\n"
                else:
                    current = section + "\n\n"

        if current.strip():
            chunks.append(self._make_chunk(current.strip(), idx, doc_id))
        return chunks

    def _tokens(self, text: str) -> int:
        return len(self.tokenizer.encode(text))

    def _get_overlap(self, text: str) -> str:
        tokens = self.tokenizer.encode(text)
        return self.tokenizer.decode(tokens[-self.overlap:])

    def _make_chunk(self, text, index, doc_id):
        return {
            "chunk_id": f"{doc_id}_chunk_{index:04d}",
            "document_id": doc_id,
            "chunk_text": text,
            "chunk_index": index,
            "token_count": self._tokens(text),
        }
```

---

## 🏷️ Chunk Data Model

```python
@dataclass
class Chunk:
    chunk_id: str          # "{doc_id}_chunk_{index}"
    document_id: str       # Parent document reference
    chunk_text: str        # The actual text content
    chunk_index: int       # Position within the document
    token_count: int       # Number of tokens
    metadata: dict         # Inherited document metadata
```

---

## 📊 Example

**Input:** "Company Refund Policy" (3 sections)  
**Output:** 2 chunks with overlap at section boundaries

```json
[
  {
    "chunk_id": "doc_001_chunk_0000",
    "chunk_text": "1. General Policy\nOur company offers a 30-day refund...",
    "chunk_index": 0,
    "token_count": 47
  },
  {
    "chunk_id": "doc_001_chunk_0001",
    "chunk_text": "...original condition.\n\n2. Exceptions\nDigital products...",
    "chunk_index": 1,
    "token_count": 62
  }
]
```

---

_← [Data Ingestion](./03-data-ingestion.md) | [Embedding Layer →](./05-embedding-layer.md)_
