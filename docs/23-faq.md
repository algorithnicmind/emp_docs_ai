# ❓ 23 — Frequently Asked Questions

> **Common questions about the Internal Docs Q&A Agent**

---

## General

### What is this project?

An AI-powered Q&A assistant that aggregates internal company documents, understands natural language questions, and provides accurate, citation-backed answers while respecting role-based access control.

### How is this different from a regular search engine?

Regular search engines use **keyword matching** — you need to know the exact terms. Our system uses **semantic search** powered by AI embeddings, so you can ask natural questions like "How do I request time off?" and get relevant results even if the document says "PTO policy."

### What types of documents are supported?

- **MVP:** PDF files, Markdown files, Plain text
- **Phase 2:** Notion pages, Google Docs, Confluence pages
- **Phase 3:** Shared drives, custom integrations

---

## Technical

### What is RAG?

**Retrieval-Augmented Generation** is an AI architecture that:

1. **Retrieves** relevant document chunks using vector similarity search
2. **Augments** the LLM prompt with this real context
3. **Generates** an answer grounded in actual company documents

This approach dramatically reduces hallucination compared to using an LLM alone.

### How does chunking work?

Documents are split into 500-1000 token segments with 50-100 token overlap between consecutive chunks. This ensures that information at chunk boundaries isn't lost and each chunk is small enough for precise embedding.

### What embedding model is used?

We use OpenAI's `text-embedding-3-small` (1536 dimensions) for converting text into vectors. This provides an excellent balance of quality and cost.

### What vector database is used?

- **MVP:** ChromaDB (local, easy setup)
- **Scale:** Can migrate to Pinecone (cloud-managed, unlimited scale)

### How does the system prevent hallucination?

1. **Low temperature** (0.1) on GPT-4 reduces creative generation
2. **Strict system prompt** instructs the model to only use provided context
3. **Citation requirement** forces the model to reference specific sources
4. **"I don't know" fallback** when no relevant context is found

---

## Access & Security

### How does role-based access work?

Every document is tagged with an `access_level` (`all`, `department`, `confidential`) and a `department`. When a user searches, the system checks their role and filters out any documents they shouldn't see **before** sending context to the LLM.

### Can confidential documents be leaked?

No. Access filtering happens at the retrieval stage (Step 4 in the query pipeline), meaning unauthorized document chunks never reach the LLM. The model simply never sees them.

### What authentication method is used?

JWT (JSON Web Tokens) for API/Web and Slack OAuth for the Slack integration.

---

## Usage

### How do I ask a question in Slack?

Type `/ask` followed by your question:

```
/ask What is the company's refund policy?
```

The bot will reply in the same channel with an answer and source citations.

### How accurate are the answers?

Accuracy depends on the quality and coverage of indexed documents. Our target is:

- **Retrieval accuracy:** > 90%
- **Response relevance:** > 85%
- **Hallucination rate:** < 5%

### What happens if the system doesn't know the answer?

The system will respond with something like: _"I don't have enough information in the indexed documents to answer this question. You may want to check with [relevant department]."_

### Can I give feedback on answers?

Yes! Every response includes 👍/👎 feedback buttons. This data helps improve the system over time.

---

## Administration

### How do I upload new documents?

1. Log into the Admin Dashboard
2. Go to **Documents → Upload**
3. Select your file (PDF, MD, or TXT)
4. Fill in metadata (title, department, access level)
5. Click **Upload** — the system will automatically process and index it

### How often are external sources synced?

- **Manual:** Anytime via the admin dashboard
- **Scheduled:** Configurable (default: every 6 hours)
- **Webhook:** Real-time when source documents are updated (Phase 2)

### How do I manage user roles?

Admin Dashboard → Users → Click on user → Update Role → Save

---

## Performance

### How fast are responses?

Average response time is 2-5 seconds, consisting of:

- Embedding: ~100ms
- Vector search: ~50ms
- RBAC filtering: ~10ms
- LLM generation: ~2-3s
- Formatting: ~50ms

### Can it handle many concurrent users?

- **MVP:** 10-50 concurrent users (single server)
- **Growth:** 50-500 with Redis caching and worker processes
- **Enterprise:** 500+ with Kubernetes and managed vector DB

---

## Troubleshooting

### The bot isn't responding in Slack

1. Check if the bot is online (green indicator)
2. Verify `SLACK_BOT_TOKEN` is valid
3. Ensure the bot has been invited to the channel
4. Check server logs for errors

### Search results seem irrelevant

1. Try rephrasing your question
2. Check if the relevant document is indexed (Admin Dashboard)
3. Verify the document's access level matches your role
4. The document may need re-indexing if recently updated

### Upload is failing

1. Check file size (max 50MB)
2. Ensure file format is supported (PDF, MD, TXT)
3. Check available disk space
4. Review server logs for specific errors

---

_← [Glossary](./22-glossary.md) | [Back to Index](./README.md)_
