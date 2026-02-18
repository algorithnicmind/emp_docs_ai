# 🏗 02 — System Architecture

> **Retrieval-Augmented Generation (RAG) Architecture**

---

## 🔍 What is RAG?

**Retrieval-Augmented Generation** is an AI framework that combines:

1. **Retrieval** — Finding relevant documents from a knowledge base
2. **Augmentation** — Using retrieved context to enhance the prompt
3. **Generation** — Producing accurate, grounded answers using an LLM

This approach significantly reduces hallucination and ensures answers are backed by actual company documents.

---

## 🏛 High-Level Architecture

```
╔══════════════════════════════════════════════════════════════════╗
║                    INTERNAL DOCS Q&A AGENT                      ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  ┌─────────────────── DATA PIPELINE ──────────────────────┐     ║
║  │                                                         │     ║
║  │  ┌──────────┐   ┌──────────┐   ┌──────────┐           │     ║
║  │  │ 1. DATA  │──▶│ 2. TEXT  │──▶│ 3. EMBED │           │     ║
║  │  │ INGEST   │   │ PROCESS  │   │ LAYER    │           │     ║
║  │  └──────────┘   └──────────┘   └────┬─────┘           │     ║
║  │                                      │                  │     ║
║  │                                      ▼                  │     ║
║  │                               ┌──────────┐             │     ║
║  │                               │ 4. VECTOR│             │     ║
║  │                               │ STORAGE  │             │     ║
║  │                               └────┬─────┘             │     ║
║  └────────────────────────────────────┼────────────────────┘     ║
║                                       │                          ║
║  ┌─────────────────── QUERY PIPELINE ─┼───────────────────┐     ║
║  │                                    │                    │     ║
║  │  ┌──────────┐   ┌──────────┐      │                   │     ║
║  │  │ 7. USER  │──▶│ 5. QUERY │──────┘                   │     ║
║  │  │ INTERFACE│   │ PROCESS  │                           │     ║
║  │  │(Slack/Web│   └────┬─────┘                           │     ║
║  │  └────▲─────┘        │                                 │     ║
║  │       │              ▼                                 │     ║
║  │       │        ┌──────────┐                            │     ║
║  │       └────────│ 6. LLM   │                            │     ║
║  │                │ GENERATE │                            │     ║
║  │                └──────────┘                            │     ║
║  └────────────────────────────────────────────────────────┘     ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 📦 Component Breakdown

### 7 Core Layers

| Layer       | Component        | Responsibility                         |
| ----------- | ---------------- | -------------------------------------- |
| **Layer 1** | Data Ingestion   | Collect documents from all sources     |
| **Layer 2** | Text Processing  | Clean, chunk, and tag documents        |
| **Layer 3** | Embedding        | Convert text to vector representations |
| **Layer 4** | Vector Storage   | Store and index embeddings             |
| **Layer 5** | Query Processing | Process user queries, retrieve context |
| **Layer 6** | LLM Generation   | Generate answers with citations        |
| **Layer 7** | Interface        | Slack bot, Web UI, Admin Dashboard     |

---

## 🔄 Data Flow — Ingestion Pipeline

```
Step 1: Document Source
    │
    ▼
Step 2: Raw Text Extraction
    │   • Extract text from PDFs, Markdown, API responses
    │   • Extract metadata (title, author, date, department)
    │
    ▼
Step 3: Text Preprocessing
    │   • Clean formatting artifacts
    │   • Normalize whitespace
    │   • Remove boilerplate
    │
    ▼
Step 4: Chunking
    │   • Split into 500–1000 token chunks
    │   • Apply 50–100 token overlap
    │   • Maintain semantic boundaries
    │
    ▼
Step 5: Embedding Generation
    │   • Convert each chunk to a dense vector
    │   • Using OpenAI text-embedding-ada-002 (1536 dims)
    │
    ▼
Step 6: Store in Vector DB
    │   • Index vector + metadata
    │   • Tag with access_level, department
    │
    ▼
Step 7: Update Document Registry
        • Record in PostgreSQL (documents table)
        • Track chunk mappings
```

---

## 🔍 Data Flow — Query Pipeline

```
Step 1: User Query (Slack / Web)
    │    "What is the refund policy for enterprise customers?"
    │
    ▼
Step 2: Query Preprocessing
    │   • Clean and normalize query
    │   • Extract intent signals
    │
    ▼
Step 3: Query Embedding
    │   • Convert question to vector (same model as indexing)
    │
    ▼
Step 4: Similarity Search
    │   • Search vector DB for Top-K similar chunks
    │   • K = 5 (configurable)
    │
    ▼
Step 5: Access Filtering (RBAC)
    │   • Check user role against chunk metadata
    │   • Remove unauthorized chunks
    │
    ▼
Step 6: Context Assembly
    │   • Combine relevant chunks into structured context
    │   • Add source metadata for citations
    │
    ▼
Step 7: LLM Prompt Construction
    │   • System instruction + Context + Question
    │
    ▼
Step 8: LLM Response Generation
    │   • GPT-4 generates answer
    │
    ▼
Step 9: Post-Processing
    │   • Format citations
    │   • Add confidence indicators
    │   • Log query for analytics
    │
    ▼
Step 10: Deliver Response
        • Send answer to Slack thread / Web UI
        • Include source links
```

---

## 🧩 Component Interaction Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Slack Bot    │  │  Web Chat    │  │  Admin Panel │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
└─────────┼─────────────────┼─────────────────┼───────────────┘
          │                 │                 │
          ▼                 ▼                 ▼
┌─────────────────────────────────────────────────────────────┐
│                     API GATEWAY                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  FastAPI / Express.js                                │    │
│  │  • Authentication (JWT)                              │    │
│  │  • Rate Limiting                                     │    │
│  │  • Request Routing                                   │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────┬───────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  Query       │ │  Ingestion   │ │  Admin       │
│  Service     │ │  Service     │ │  Service     │
│              │ │              │ │              │
│ • Embed query│ │ • Parse docs │ │ • CRUD docs  │
│ • Search DB  │ │ • Chunk text │ │ • Manage     │
│ • Filter RBAC│ │ • Generate   │ │   users/roles│
│ • Call LLM   │ │   embeddings │ │ • Analytics  │
│ • Format     │ │ • Store in   │ │              │
│   response   │ │   vector DB  │ │              │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────┐
│                      DATA LAYER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Vector DB   │  │  PostgreSQL  │  │  Redis Cache │      │
│  │  (FAISS/     │  │  (Metadata,  │  │  (Query      │      │
│  │   Chroma)    │  │   Users,     │  │   Cache,     │      │
│  │              │  │   Logs)      │  │   Sessions)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
emp_docs_ai/
├── docs/                      # 📚 Project documentation
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI application entry
│   │   ├── config.py          # Configuration management
│   │   ├── models/            # Database models (SQLAlchemy)
│   │   │   ├── user.py
│   │   │   ├── document.py
│   │   │   ├── chunk.py
│   │   │   └── query_log.py
│   │   ├── services/          # Business logic
│   │   │   ├── ingestion.py   # Document ingestion
│   │   │   ├── chunking.py    # Text processing
│   │   │   ├── embedding.py   # Embedding generation
│   │   │   ├── retrieval.py   # Vector search
│   │   │   ├── generation.py  # LLM response
│   │   │   └── rbac.py        # Access control
│   │   ├── api/               # API routes
│   │   │   ├── auth.py
│   │   │   ├── query.py
│   │   │   ├── documents.py
│   │   │   └── admin.py
│   │   ├── integrations/      # External integrations
│   │   │   ├── slack.py
│   │   │   ├── notion.py
│   │   │   └── gdocs.py
│   │   └── utils/             # Shared utilities
│   │       ├── logger.py
│   │       └── helpers.py
│   ├── tests/                 # Test suite
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                  # Admin Dashboard (React/Next.js)
│   ├── src/
│   ├── public/
│   └── package.json
├── vector_store/              # Local vector DB storage
├── scripts/                   # Utility scripts
│   ├── seed_data.py
│   └── sync_docs.py
├── .env.example
├── docker-compose.yml
├── README.md
└── LICENSE
```

---

## 🔧 Technology Choices

| Component         | Technology              | Justification                          |
| ----------------- | ----------------------- | -------------------------------------- |
| **Backend API**   | FastAPI (Python)        | Async, fast, auto-docs, ML-friendly    |
| **Vector DB**     | FAISS / ChromaDB        | Open-source, local-first, easy setup   |
| **Relational DB** | PostgreSQL              | Robust, reliable, ACID-compliant       |
| **Cache**         | Redis                   | In-memory caching for frequent queries |
| **LLM**           | OpenAI GPT-4            | Best-in-class generation quality       |
| **Embeddings**    | OpenAI Ada-002          | High quality, 1536 dimensions          |
| **Frontend**      | React + Next.js         | Modern, fast, great DX                 |
| **Bot**           | Slack Bolt SDK          | Official SDK, event-driven             |
| **Auth**          | JWT + OAuth 2.0         | Industry standard, secure              |
| **Deployment**    | Docker + Docker Compose | Portable, reproducible                 |

---

## 🔐 Security Architecture

```
┌─────────────────────────────────────────────┐
│              SECURITY LAYERS                │
│                                             │
│  Layer 1: Network Security                  │
│  ├── HTTPS/TLS encryption                   │
│  ├── API rate limiting                      │
│  └── CORS configuration                    │
│                                             │
│  Layer 2: Authentication                    │
│  ├── JWT token-based auth                   │
│  ├── Slack OAuth integration                │
│  └── Session management                    │
│                                             │
│  Layer 3: Authorization (RBAC)              │
│  ├── Role-based access control              │
│  ├── Document-level permissions             │
│  └── Pre-LLM access filtering              │
│                                             │
│  Layer 4: Data Security                     │
│  ├── Encrypted storage (at rest)            │
│  ├── Encrypted transmission (in transit)    │
│  └── API key management                    │
└─────────────────────────────────────────────┘
```

---

## 📊 Scalability Tiers

| Tier           | Team Size | Vector DB        | Deployment     | Notes         |
| -------------- | --------- | ---------------- | -------------- | ------------- |
| **Small**      | 1-50      | FAISS (local)    | Single server  | Hackathon MVP |
| **Medium**     | 50-500    | Chroma (managed) | Docker Compose | Startup scale |
| **Enterprise** | 500+      | Pinecone         | Kubernetes     | Microservices |

---

_← [Project Overview](./01-project-overview.md) | [Data Ingestion →](./03-data-ingestion.md)_
