# 🗃️ 11 — Database Design

> **Relational database schema for metadata, users, and query logs**

---

## 🎯 Purpose

While embeddings live in the Vector DB, we need a relational database (PostgreSQL) for:

- User management and authentication
- Document metadata tracking
- Chunk references
- Query logging and analytics
- Role-based access control

---

## 📊 Entity Relationship Diagram

```
┌─────────────┐       ┌──────────────────┐       ┌──────────────┐
│   USERS     │       │    DOCUMENTS     │       │    CHUNKS    │
├─────────────┤       ├──────────────────┤       ├──────────────┤
│ id (PK)     │       │ id (PK)          │       │ id (PK)      │
│ name        │       │ title            │       │ document_id  │──┐
│ email       │       │ source           │       │   (FK)       │  │
│ role        │       │ department       │       │ chunk_text   │  │
│ slack_id    │       │ access_level     │       │ chunk_index  │  │
│ created_at  │       │ author           │       │ embedding_ref│  │
│ updated_at  │       │ file_type        │       │ token_count  │  │
└──────┬──────┘       │ file_path        │       │ created_at   │  │
       │              │ word_count       │       └──────────────┘  │
       │              │ created_at       │              │           │
       │              │ updated_at       │◀─────────────┘           │
       │              └──────────────────┘                         │
       │                                                           │
       │              ┌──────────────────┐                         │
       │              │   QUERY_LOGS     │                         │
       │              ├──────────────────┤                         │
       └─────────────▶│ id (PK)          │                         │
                      │ user_id (FK)     │                         │
                      │ question         │                         │
                      │ response         │                         │
                      │ sources_used     │                         │
                      │ similarity_score │                         │
                      │ response_time_ms │                         │
                      │ feedback_score   │                         │
                      │ timestamp        │                         │
                      └──────────────────┘                         │
                                                                   │
                      ┌──────────────────┐                         │
                      │  DATA_SOURCES    │                         │
                      ├──────────────────┤                         │
                      │ id (PK)          │                         │
                      │ name             │                         │
                      │ type             │                         │
                      │ config (JSON)    │                         │
                      │ last_sync        │                         │
                      │ status           │                         │
                      │ created_at       │                         │
                      └──────────────────┘
```

---

## 📋 Table Definitions

### Users Table

```sql
CREATE TABLE users (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name          VARCHAR(255) NOT NULL,
    email         VARCHAR(255) UNIQUE NOT NULL,
    role          VARCHAR(50) NOT NULL DEFAULT 'general',
    slack_id      VARCHAR(50) UNIQUE,
    password_hash VARCHAR(255),
    department    VARCHAR(100),
    is_active     BOOLEAN DEFAULT TRUE,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_role CHECK (role IN (
        'admin', 'hr', 'engineering', 'finance', 'general'
    ))
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_slack_id ON users(slack_id);
CREATE INDEX idx_users_role ON users(role);
```

### Documents Table

```sql
CREATE TABLE documents (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title         VARCHAR(500) NOT NULL,
    source        VARCHAR(50) NOT NULL,
    department    VARCHAR(100) NOT NULL DEFAULT 'general',
    access_level  VARCHAR(50) NOT NULL DEFAULT 'all',
    author        VARCHAR(255),
    file_type     VARCHAR(20),
    file_path     TEXT,
    source_url    TEXT,
    word_count    INTEGER,
    chunk_count   INTEGER DEFAULT 0,
    status        VARCHAR(20) DEFAULT 'processing',
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_access CHECK (access_level IN (
        'all', 'department', 'confidential'
    )),
    CONSTRAINT chk_source CHECK (source IN (
        'pdf_upload', 'markdown', 'notion', 'google_docs',
        'confluence', 'plain_text'
    )),
    CONSTRAINT chk_status CHECK (status IN (
        'processing', 'indexed', 'failed', 'deleted'
    ))
);

CREATE INDEX idx_docs_department ON documents(department);
CREATE INDEX idx_docs_access ON documents(access_level);
CREATE INDEX idx_docs_source ON documents(source);
CREATE INDEX idx_docs_status ON documents(status);
```

### Chunks Table

```sql
CREATE TABLE chunks (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id     UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_text      TEXT NOT NULL,
    chunk_index     INTEGER NOT NULL,
    embedding_ref   VARCHAR(255),
    token_count     INTEGER,
    section_heading VARCHAR(500),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(document_id, chunk_index)
);

CREATE INDEX idx_chunks_document ON chunks(document_id);
```

### Query Logs Table

```sql
CREATE TABLE query_logs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES users(id),
    question        TEXT NOT NULL,
    response        TEXT,
    sources_used    JSONB,
    similarity_score FLOAT,
    response_time_ms INTEGER,
    feedback_score  INTEGER,
    model_used      VARCHAR(50),
    tokens_used     INTEGER,
    timestamp       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_queries_user ON query_logs(user_id);
CREATE INDEX idx_queries_timestamp ON query_logs(timestamp);
CREATE INDEX idx_queries_feedback ON query_logs(feedback_score);
```

### Data Sources Table

```sql
CREATE TABLE data_sources (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        VARCHAR(255) NOT NULL,
    type        VARCHAR(50) NOT NULL,
    config      JSONB,
    last_sync   TIMESTAMP,
    status      VARCHAR(20) DEFAULT 'active',
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔗 SQLAlchemy Models

```python
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    role = Column(String(50), default="general")
    slack_id = Column(String(50), unique=True)
    queries = relationship("QueryLog", back_populates="user")

class Document(Base):
    __tablename__ = "documents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)
    source = Column(String(50), nullable=False)
    department = Column(String(100), default="general")
    access_level = Column(String(50), default="all")
    chunks = relationship("Chunk", back_populates="document", cascade="all, delete")

class Chunk(Base):
    __tablename__ = "chunks"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"))
    chunk_text = Column(String, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    document = relationship("Document", back_populates="chunks")

class QueryLog(Base):
    __tablename__ = "query_logs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    question = Column(String, nullable=False)
    response = Column(String)
    feedback_score = Column(Integer)
    user = relationship("User", back_populates="queries")
```

---

_← [RBAC](./10-rbac.md) | [Admin Dashboard →](./12-admin-dashboard.md)_
