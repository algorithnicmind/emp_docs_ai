# 📖 22 — Glossary

> **Key terms, acronyms, and definitions**

---

## A

| Term             | Definition                                                                     |
| ---------------- | ------------------------------------------------------------------------------ |
| **Access Level** | Permission tier assigned to a document: `all`, `department`, or `confidential` |
| **API**          | Application Programming Interface — standard way for software to communicate   |
| **Async**        | Asynchronous programming — non-blocking execution for better performance       |

## B

| Term                 | Definition                                                                  |
| -------------------- | --------------------------------------------------------------------------- |
| **Batch Processing** | Processing multiple items together in a single operation                    |
| **Bearer Token**     | Authentication token sent in HTTP headers (`Authorization: Bearer <token>`) |

## C

| Term                  | Definition                                                                      |
| --------------------- | ------------------------------------------------------------------------------- |
| **Chunk**             | A segment of text extracted from a larger document (500-1000 tokens)            |
| **Chunking**          | The process of splitting documents into smaller, manageable pieces              |
| **ChromaDB**          | An open-source vector database for storing and querying embeddings              |
| **Citation**          | Reference to the source document from which an answer was derived               |
| **Cosine Similarity** | A metric measuring the angle between two vectors (1 = identical, 0 = unrelated) |
| **CORS**              | Cross-Origin Resource Sharing — browser security mechanism for API requests     |
| **CSAT**              | Customer Satisfaction Score — user satisfaction metric                          |

## D

| Term             | Definition                                                                    |
| ---------------- | ----------------------------------------------------------------------------- |
| **Dense Vector** | A numerical array where most values are non-zero (vs sparse vectors)          |
| **Document**     | Any piece of content indexed in the system (PDF, Markdown, Notion page, etc.) |

## E

| Term                | Definition                                                           |
| ------------------- | -------------------------------------------------------------------- |
| **Embedding**       | A dense vector representation of text that captures semantic meaning |
| **Embedding Model** | An AI model that converts text to vectors (e.g., OpenAI Ada-002)     |

## F

| Term        | Definition                                                                |
| ----------- | ------------------------------------------------------------------------- |
| **FAISS**   | Facebook AI Similarity Search — library for fast vector similarity search |
| **FastAPI** | Modern Python web framework for building APIs                             |

## G

| Term           | Definition                                                                     |
| -------------- | ------------------------------------------------------------------------------ |
| **GPT-4**      | OpenAI's large language model used for generating answers                      |
| **Guardrails** | Rules that prevent the AI from generating inappropriate or incorrect responses |

## H

| Term              | Definition                                                                             |
| ----------------- | -------------------------------------------------------------------------------------- |
| **Hallucination** | When an LLM generates information not supported by source documents                    |
| **HNSW**          | Hierarchical Navigable Small World — algorithm for approximate nearest neighbor search |

## J

| Term    | Definition                                                        |
| ------- | ----------------------------------------------------------------- |
| **JWT** | JSON Web Token — compact, self-contained token for authentication |

## K

| Term               | Definition                                               |
| ------------------ | -------------------------------------------------------- |
| **Knowledge Base** | The collection of all indexed documents and their chunks |

## L

| Term    | Definition                                                              |
| ------- | ----------------------------------------------------------------------- |
| **LLM** | Large Language Model — AI model trained on vast text data (e.g., GPT-4) |

## M

| Term         | Definition                                                             |
| ------------ | ---------------------------------------------------------------------- |
| **Metadata** | Information about a document (title, author, department, access level) |
| **MVP**      | Minimum Viable Product — first working version with core features      |

## O

| Term        | Definition                                                               |
| ----------- | ------------------------------------------------------------------------ |
| **Overlap** | Shared text between consecutive chunks to preserve context at boundaries |

## P

| Term                   | Definition                                                           |
| ---------------------- | -------------------------------------------------------------------- |
| **Pinecone**           | Cloud-managed vector database for production deployments             |
| **Prompt Engineering** | Crafting effective instructions for LLMs to generate desired outputs |

## R

| Term            | Definition                                                                        |
| --------------- | --------------------------------------------------------------------------------- |
| **RAG**         | Retrieval-Augmented Generation — combining document retrieval with LLM generation |
| **RBAC**        | Role-Based Access Control — permissions system based on user roles                |
| **Re-indexing** | Reprocessing a document to update its chunks and embeddings                       |
| **Retrieval**   | Finding relevant document chunks based on a user query                            |

## S

| Term                 | Definition                                                            |
| -------------------- | --------------------------------------------------------------------- |
| **Semantic Search**  | Search based on meaning rather than exact keyword matching            |
| **Similarity Score** | Numerical measure of how closely two vectors match (0 to 1)           |
| **SSE**              | Server-Sent Events — one-way streaming from server to client          |
| **Streaming**        | Sending the LLM response token-by-token for faster perceived response |

## T

| Term      | Definition                                                            |
| --------- | --------------------------------------------------------------------- |
| **Token** | The basic unit text is broken into for LLM processing (≈ ¾ of a word) |
| **Top-K** | The number of most similar results retrieved from vector search       |

## V

| Term                | Definition                                                                     |
| ------------------- | ------------------------------------------------------------------------------ |
| **Vector**          | A list of numbers representing text in multi-dimensional space                 |
| **Vector Database** | Specialized database for storing and searching vectors (e.g., ChromaDB, FAISS) |
| **Vector Space**    | Mathematical space where embeddings exist; similar texts are near each other   |

## W

| Term        | Definition                                                                   |
| ----------- | ---------------------------------------------------------------------------- |
| **Webhook** | HTTP callback triggered by an event (e.g., document updated → auto re-index) |

---

_← [Contributing](./21-contributing.md) | [FAQ →](./23-faq.md)_
