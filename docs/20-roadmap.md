# 🗺️ 20 — Project Roadmap

> **Milestones, phases, and future plans**

---

## 📅 Development Phases

### Phase 1: MVP (Hackathon) — Week 1-2

**Goal:** Working prototype with core RAG pipeline

| Task                             | Status | Priority |
| -------------------------------- | ------ | -------- |
| Project setup & structure        | ✅     | P0       |
| Documentation (docs/)            | ✅     | P0       |
| PDF & Markdown ingestion         | ✅     | P0       |
| Text chunking with overlap       | ✅     | P0       |
| OpenAI embedding generation      | ✅     | P0       |
| ChromaDB vector storage          | ✅     | P0       |
| Semantic search (query pipeline) | ✅     | P0       |
| GPT-4 response generation        | ✅     | P0       |
| Basic RBAC (role filtering)      | ✅     | P0       |
| REST API endpoints               | ✅     | P0       |
| Slack bot (basic /ask)           | ✅     | P1       |
| Basic admin dashboard API        | ✅     | P1       |
| JWT authentication               | ✅     | P0       |

**Deliverable:** Demo-ready Q&A agent with PDF/MD support ✅

---

### Phase 2: Enhancement — Week 3-4

**Goal:** Production-quality features and reliability

| Task                            | Status | Priority |
| ------------------------------- | ------ | -------- |
| Redis query caching             | ✅     | P1       |
| Streaming responses (SSE)       | ✅     | P1       |
| Query analytics dashboard API   | ✅     | P1       |
| User feedback collection        | ✅     | P1       |
| Document management API         | ✅     | P1       |
| Batch embedding optimization    | ✅     | P2       |
| Error handling & logging        | ✅     | P1       |
| Unit & integration tests        | ✅     | P1       |
| CI/CD pipeline (GitHub Actions) | ✅     | P2       |
| Alembic database migrations     | ✅     | P1       |
| Docker Compose setup            | ✅     | P1       |
| Background processing (Celery)  | 🔲     | P2       |

**Deliverable:** Optimized system with analytics and caching

---

### Phase 3: Integrations & Frontend (Weeks 5-6)

**Goal:** Connect to all major document sources and deliver a working frontend

- [x] Frontend Web Chat UI (Next.js) ✅
  - [x] Login Page with Auth Context ✅
  - [x] RAG Chat Interface (Markdown support) ✅
  - [x] Responsive Sidebar & Layout ✅
- [x] Admin Dashboard UI (MVP) ✅
  - [x] Statistics Overview Page ✅
  - [x] Documents List View ✅
- [ ] Connect Data Sources (Settings Page)
- [ ] Slack Bot Integration (Bolt)
- [ ] Confluence / Notion Connectors
- [ ] Notion API integration
- [ ] Google Docs API integration
- [ ] Confluence API integration
- [ ] Webhook-based auto re-indexing
- [ ] Scheduled sync (cron)
- [ ] Source management UI

**Deliverable:** Multi-source document ingestion + web frontend

---

### Phase 4: Enterprise Ready — Month 3+

**Goal:** Scalable, secure, enterprise-grade system

| Task                           | Status | Priority |
| ------------------------------ | ------ | -------- |
| Pinecone vector DB migration   | 🔲     | P2       |
| SSO / SAML authentication      | 🔲     | P2       |
| Advanced RBAC (custom roles)   | 🔲     | P2       |
| Audit logging                  | 🔲     | P2       |
| Multi-language support         | 🔲     | P3       |
| Kubernetes deployment          | 🔲     | P2       |
| Load testing (100+ concurrent) | 🔲     | P2       |
| SOC 2 compliance prep          | 🔲     | P3       |
| Multi-region deployment        | 🔲     | P3       |

---

## 🏆 Key Milestones

```
Week 1  ──▶  Project setup + docs + basic ingestion               ✅
Week 2  ──▶  Full RAG pipeline working end-to-end                 ✅
Week 3  ──▶  Caching + Testing + CI/CD + Docker                   ✅
Week 4  ──▶  Frontend Web Chat + Admin Dashboard                  🔲
Month 2 ──▶  Multi-source integrations                            🔲
Month 3 ──▶  Enterprise features + scale                          🔲
```

---

## 📊 Success Criteria (Hackathon MVP)

| Criteria                           | Target     |
| ---------------------------------- | ---------- |
| Upload a PDF and query it          | ✅ Working |
| Get accurate answer with citations | ✅ Working |
| RBAC filters unauthorized docs     | ✅ Working |
| Slack /ask command works           | ✅ Working |
| Response time < 10s                | ✅ Met     |
| Admin can upload/manage docs       | ✅ Working |
| Redis caching for repeat queries   | ✅ Working |
| Streaming responses via SSE        | ✅ Working |
| 23+ passing unit/integration tests | ✅ Working |

---

_← [Tech Stack](./19-tech-stack.md) | [Contributing →](./21-contributing.md)_
