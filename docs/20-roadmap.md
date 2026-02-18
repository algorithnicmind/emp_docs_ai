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
| PDF & Markdown ingestion         | 🔲     | P0       |
| Text chunking with overlap       | 🔲     | P0       |
| OpenAI embedding generation      | 🔲     | P0       |
| ChromaDB vector storage          | 🔲     | P0       |
| Semantic search (query pipeline) | 🔲     | P0       |
| GPT-4 response generation        | 🔲     | P0       |
| Basic RBAC (role filtering)      | 🔲     | P0       |
| REST API endpoints               | 🔲     | P0       |
| Slack bot (basic /ask)           | 🔲     | P1       |
| Basic admin dashboard            | 🔲     | P1       |
| JWT authentication               | 🔲     | P0       |

**Deliverable:** Demo-ready Q&A agent with PDF/MD support

---

### Phase 2: Enhancement — Week 3-4

**Goal:** Production-quality features and reliability

| Task                           | Status | Priority |
| ------------------------------ | ------ | -------- |
| Redis query caching            | 🔲     | P1       |
| Streaming responses (SSE)      | 🔲     | P1       |
| Query analytics dashboard      | 🔲     | P1       |
| User feedback collection       | 🔲     | P1       |
| Document management UI         | 🔲     | P1       |
| Batch embedding optimization   | 🔲     | P2       |
| Background processing (Celery) | 🔲     | P1       |
| Error handling & logging       | 🔲     | P1       |
| Unit & integration tests       | 🔲     | P1       |
| CI/CD pipeline                 | 🔲     | P2       |

**Deliverable:** Optimized system with analytics and caching

---

### Phase 3: Integrations — Month 2

**Goal:** Connect to all major document sources

| Task                           | Status | Priority |
| ------------------------------ | ------ | -------- |
| Notion API integration         | 🔲     | P1       |
| Google Docs API integration    | 🔲     | P1       |
| Confluence API integration     | 🔲     | P2       |
| Webhook-based auto re-indexing | 🔲     | P2       |
| Scheduled sync (cron)          | 🔲     | P2       |
| Source management UI           | 🔲     | P2       |

**Deliverable:** Multi-source document ingestion

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
| Docker/Kubernetes deployment   | 🔲     | P2       |
| Load testing (100+ concurrent) | 🔲     | P2       |
| SOC 2 compliance prep          | 🔲     | P3       |
| Multi-region deployment        | 🔲     | P3       |

---

## 🏆 Key Milestones

```
Week 1  ──▶  Project setup + docs + basic ingestion
Week 2  ──▶  Full RAG pipeline working end-to-end
Week 3  ──▶  Slack bot + admin dashboard live
Week 4  ──▶  Caching + analytics + feedback
Month 2 ──▶  Multi-source integrations
Month 3 ──▶  Enterprise features + scale
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

---

_← [Tech Stack](./19-tech-stack.md) | [Contributing →](./21-contributing.md)_
