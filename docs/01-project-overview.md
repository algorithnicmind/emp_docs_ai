# 📖 01 — Project Overview

> **Internal Docs Q&A Agent for Teams**

---

## 🎯 Core Objective

Build an AI-powered assistant that:

- ✅ **Aggregates** internal documents from multiple sources (Notion, Google Docs, Confluence, PDFs, Shared Drives)
- ✅ **Understands** natural language queries using semantic search
- ✅ **Retrieves** relevant company information with high accuracy
- ✅ **Responds** inside team tools (Slack, Web Dashboard)
- ✅ **Provides** source-backed, citation-rich answers
- ✅ **Respects** role-based permissions for secure information retrieval

---

## 🧠 Problem Definition

### Current Situation

Enterprise knowledge is **scattered** across multiple platforms:

| Platform          | Type         | Challenge                       |
| ----------------- | ------------ | ------------------------------- |
| **Notion**        | Wiki / Docs  | Siloed workspaces, deep nesting |
| **Google Docs**   | Documents    | Scattered across shared drives  |
| **Confluence**    | Wiki         | Complex permission hierarchies  |
| **PDFs**          | Static Files | Unsearchable, version chaos     |
| **Shared Drives** | Mixed Files  | Unstructured, hard to navigate  |

### The Pain Points

```
┌──────────────────────────────────────────────────────┐
│                    CURRENT STATE                     │
│                                                      │
│  👤 Employee has a question                          │
│       │                                              │
│       ├──▶ Search Notion → Not found                 │
│       ├──▶ Search Confluence → Outdated info         │
│       ├──▶ Search Google Drive → Too many results    │
│       ├──▶ Ask colleague → They don't know either    │
│       └──▶ Ask manager → Takes hours to respond      │
│                                                      │
│  ⏱️  Average time wasted: 30-60 minutes per query   │
│  📉  Productivity loss: ~20% of work hours           │
└──────────────────────────────────────────────────────┘
```

### Impact of the Problem

| Metric                   | Impact                                                       |
| ------------------------ | ------------------------------------------------------------ |
| **Time Wasted**          | Employees spend 20%+ of their time searching for information |
| **Duplicate Questions**  | Same questions asked repeatedly across channels              |
| **Outdated Information** | Decisions based on stale docs lead to costly errors          |
| **Onboarding Delays**    | New hires take weeks to find essential documentation         |
| **Knowledge Silos**      | Critical knowledge locked in individual team members         |

---

## 💡 Our Solution

### The Internal Docs Q&A Agent

```
┌──────────────────────────────────────────────────────┐
│                   PROPOSED STATE                     │
│                                                      │
│  👤 Employee has a question                          │
│       │                                              │
│       └──▶ Types /ask "What's the refund policy?"    │
│                │                                     │
│                ▼                                     │
│       ┌─────────────────┐                            │
│       │  🤖 Q&A Agent    │                           │
│       │  • Searches all  │                           │
│       │    sources       │                           │
│       │  • Checks access │                           │
│       │  • Generates     │                           │
│       │    answer        │                           │
│       └────────┬────────┘                            │
│                │                                     │
│                ▼                                     │
│       📝 Answer with citations in <10 seconds        │
│                                                      │
│  ⏱️  Average response time: 5-10 seconds            │
│  📈  Productivity gain: ~15-20% recovered            │
└──────────────────────────────────────────────────────┘
```

---

## 🏆 Key Features (Core)

| #   | Feature                     | Description                                                   |
| --- | --------------------------- | ------------------------------------------------------------- |
| 1   | **Semantic Search**         | AI-powered search that understands meaning, not just keywords |
| 2   | **Citation-Backed Answers** | Every response includes source links for verification         |
| 3   | **Role-Aware Retrieval**    | Answers respect department and access-level permissions       |
| 4   | **Slack Integration**       | Ask questions directly in Slack with `/ask` command           |
| 5   | **Auto Document Indexing**  | Documents are automatically ingested and indexed              |
| 6   | **Query Analytics**         | Track what questions are most asked, identify knowledge gaps  |
| 7   | **Multi-Source Support**    | Pulls from Notion, Google Docs, Confluence, PDFs, and more    |
| 8   | **Admin Dashboard**         | Centralized management for documents, users, and analytics    |

---

## 🎯 Target Users

| Role                 | How They Use It                                         |
| -------------------- | ------------------------------------------------------- |
| **General Employee** | Ask questions via Slack, get instant answers            |
| **HR Team**          | Query policies, onboarding docs, compliance info        |
| **Engineering Team** | Search technical docs, architecture decisions, runbooks |
| **Finance Team**     | Look up financial policies, budget guidelines           |
| **Managers**         | Get summaries, track team knowledge gaps                |
| **Admins**           | Upload docs, manage access, monitor system health       |

---

## 📊 Success Metrics

| Metric                   | Target                      |
| ------------------------ | --------------------------- |
| **Response Time**        | < 10 seconds                |
| **Retrieval Accuracy**   | > 90%                       |
| **User Satisfaction**    | > 4.5/5 rating              |
| **Hallucination Rate**   | < 5%                        |
| **Daily Active Users**   | > 60% of team (post-launch) |
| **Time Saved per Query** | > 20 minutes average        |

---

## 🧩 Competitive Advantage

Compared to a basic chatbot, our system offers:

| Feature                    | Basic Chatbot | Our System |
| -------------------------- | :-----------: | :--------: |
| Multi-source indexing      |      ❌       |     ✅     |
| Citation-based answers     |      ❌       |     ✅     |
| Role-based filtering       |      ❌       |     ✅     |
| Enterprise-grade structure |      ❌       |     ✅     |
| Semantic search            |      ❌       |     ✅     |
| Query analytics            |      ❌       |     ✅     |
| Auto re-indexing           |      ❌       |     ✅     |

---

## 📐 Project Scope

### In Scope (Hackathon MVP)

- [x] Document ingestion from PDF and Markdown
- [x] Text chunking with overlap
- [x] Embedding generation (OpenAI)
- [x] Vector storage (FAISS / Chroma)
- [x] Semantic search & retrieval
- [x] LLM-powered response generation
- [x] Slack bot integration
- [x] Basic RBAC
- [x] Admin dashboard (basic)

### Out of Scope (Future Phases)

- [ ] Notion API integration
- [ ] Google Docs API integration
- [ ] Confluence API integration
- [ ] Real-time webhook sync
- [ ] Multi-language support
- [ ] Voice query support
- [ ] Advanced analytics dashboard
- [ ] SOC 2 compliance
- [ ] Multi-region deployment

---

_Next: [System Architecture →](./02-system-architecture.md)_
