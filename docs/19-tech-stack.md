# 🛠️ 19 — Tech Stack

> **Complete technology breakdown**

---

## 🏗️ Full Stack Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      TECH STACK                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  FRONTEND          │  BACKEND           │  AI / ML           │
│  ─────────         │  ────────          │  ───────           │
│  React 18          │  FastAPI           │  OpenAI GPT-4      │
│  Next.js 14        │  Python 3.11       │  text-embedding-3  │
│  TypeScript        │  SQLAlchemy        │  tiktoken          │
│  Tailwind CSS      │  Alembic           │  LangChain (opt)   │
│                    │  Pydantic          │                    │
│                    │                    │                    │
│  DATABASES         │  INFRASTRUCTURE    │  INTEGRATIONS      │
│  ──────────        │  ──────────────    │  ────────────      │
│  PostgreSQL 15     │  Docker            │  Slack Bolt SDK    │
│  ChromaDB          │  Docker Compose    │  Notion API        │
│  Redis 7           │  GitHub Actions    │  Google Docs API   │
│  FAISS             │  Nginx             │  Confluence API    │
│                    │                    │                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Backend Dependencies

### Core

| Package      | Version | Purpose                 |
| ------------ | ------- | ----------------------- |
| `fastapi`    | 0.109+  | Web framework           |
| `uvicorn`    | 0.27+   | ASGI server             |
| `pydantic`   | 2.5+    | Data validation         |
| `sqlalchemy` | 2.0+    | ORM                     |
| `alembic`    | 1.13+   | Database migrations     |
| `asyncpg`    | 0.29+   | Async PostgreSQL driver |

### AI / ML

| Package      | Version | Purpose                |
| ------------ | ------- | ---------------------- |
| `openai`     | 1.10+   | GPT-4 & embeddings API |
| `tiktoken`   | 0.5+    | Token counting         |
| `chromadb`   | 0.4+    | Vector database        |
| `faiss-cpu`  | 1.7+    | Local vector search    |
| `pdfplumber` | 0.10+   | PDF text extraction    |

### Auth & Security

| Package           | Version | Purpose          |
| ----------------- | ------- | ---------------- |
| `python-jose`     | 3.3+    | JWT handling     |
| `passlib[bcrypt]` | 1.7+    | Password hashing |
| `slowapi`         | 0.1+    | Rate limiting    |

### Integrations

| Package      | Version | Purpose           |
| ------------ | ------- | ----------------- |
| `slack-bolt` | 1.18+   | Slack bot SDK     |
| `redis`      | 5.0+    | Caching           |
| `celery`     | 5.3+    | Background tasks  |
| `httpx`      | 0.26+   | Async HTTP client |

---

## 🎨 Frontend Dependencies

| Package          | Version | Purpose            |
| ---------------- | ------- | ------------------ |
| `react`          | 18+     | UI library         |
| `next`           | 14+     | React framework    |
| `typescript`     | 5+      | Type safety        |
| `tailwindcss`    | 3.4+    | Styling            |
| `axios`          | 1.6+    | HTTP client        |
| `recharts`       | 2.10+   | Analytics charts   |
| `react-markdown` | 9+      | Markdown rendering |
| `lucide-react`   | 0.300+  | Icon library       |

---

## 🗄️ Database Technologies

| Database       | Type       | Purpose           | Data Stored            |
| -------------- | ---------- | ----------------- | ---------------------- |
| **PostgreSQL** | Relational | Structured data   | Users, Documents, Logs |
| **ChromaDB**   | Vector     | Similarity search | Embeddings + metadata  |
| **Redis**      | Key-Value  | Caching           | Query cache, sessions  |

---

## 🔧 Development Tools

| Tool         | Purpose             |
| ------------ | ------------------- |
| **Git**      | Version control     |
| **Docker**   | Containerization    |
| **VS Code**  | IDE                 |
| **Postman**  | API testing         |
| **pgAdmin**  | Database management |
| **pytest**   | Python testing      |
| **ESLint**   | JS/TS linting       |
| **Prettier** | Code formatting     |

---

## 📋 requirements.txt

```txt
# Core
fastapi==0.109.2
uvicorn[standard]==0.27.1
pydantic==2.6.1
sqlalchemy==2.0.25
alembic==1.13.1
asyncpg==0.29.0

# AI / ML
openai==1.12.0
tiktoken==0.5.2
chromadb==0.4.22
pdfplumber==0.10.4

# Auth
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# Integrations
slack-bolt==1.18.1
redis==5.0.1
celery==5.3.6
httpx==0.26.0

# Utils
python-dotenv==1.0.1
slowapi==0.1.9
beautifulsoup4==4.12.3

# Testing
pytest==8.0.0
pytest-asyncio==0.23.4
pytest-cov==4.1.0
```

---

_← [Evaluation Metrics](./18-evaluation-metrics.md) | [Roadmap →](./20-roadmap.md)_
