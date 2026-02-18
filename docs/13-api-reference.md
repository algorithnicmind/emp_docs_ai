# 📡 13 — API Reference

> **Complete REST API endpoint documentation**

---

## 🔗 Base URL

```
Development: http://localhost:8000/api/v1
Production:  https://api.yourdomain.com/api/v1
```

---

## 🔐 Authentication

All API requests (except `/auth/login` and `/auth/register`) require a JWT token:

```
Authorization: Bearer <jwt_token>
```

---

## 📋 Endpoints

### Authentication

#### `POST /auth/register`

Register a new user.

| Field        | Type   | Required | Description      |
| ------------ | ------ | -------- | ---------------- |
| `name`       | string | ✅       | Full name        |
| `email`      | string | ✅       | Email address    |
| `password`   | string | ✅       | Min 8 characters |
| `department` | string | ❌       | Department name  |

**Response:** `201 Created`

```json
{
  "id": "uuid",
  "name": "John Doe",
  "email": "john@company.com",
  "role": "general",
  "token": "jwt_token"
}
```

#### `POST /auth/login`

Authenticate and receive JWT token.

| Field      | Type   | Required |
| ---------- | ------ | -------- |
| `email`    | string | ✅       |
| `password` | string | ✅       |

**Response:** `200 OK`

```json
{
  "token": "jwt_token",
  "user": { "id": "uuid", "name": "John", "role": "general" }
}
```

---

### Query

#### `POST /query`

Ask a question and get an AI-generated answer.

| Field      | Type    | Required | Description                    |
| ---------- | ------- | -------- | ------------------------------ |
| `question` | string  | ✅       | Natural language question      |
| `top_k`    | integer | ❌       | Number of sources (default: 5) |

**Response:** `200 OK`

```json
{
  "query_id": "uuid",
  "answer": "The refund policy allows returns within 30 days [Source 1]...",
  "sources": [
    {
      "index": 1,
      "title": "Refund Policy",
      "source": "pdf_upload",
      "document_id": "uuid"
    }
  ],
  "confidence": "high",
  "response_time_ms": 2340
}
```

#### `POST /query/feedback`

Submit feedback for a query response.

| Field      | Type    | Required |
| ---------- | ------- | -------- | ------- |
| `query_id` | string  | ✅       |
| `score`    | integer | ✅       | -1 or 1 |
| `comment`  | string  | ❌       |

---

### Documents

#### `GET /documents`

List all documents accessible to the current user.

**Query Params:** `?page=1&limit=20&department=hr&source=pdf_upload`

**Response:** `200 OK`

```json
{
  "documents": [
    {
      "id": "uuid",
      "title": "HR Handbook",
      "source": "pdf_upload",
      "department": "hr",
      "status": "indexed",
      "chunk_count": 45,
      "created_at": "2026-02-18T10:00:00Z"
    }
  ],
  "total": 1247,
  "page": 1,
  "pages": 63
}
```

#### `POST /documents/upload` (Admin)

Upload and index a new document.

**Content-Type:** `multipart/form-data`

| Field          | Type   | Required |
| -------------- | ------ | -------- |
| `file`         | file   | ✅       |
| `title`        | string | ✅       |
| `department`   | string | ✅       |
| `access_level` | string | ❌       |

**Response:** `201 Created`

```json
{
  "id": "uuid",
  "title": "New Policy",
  "status": "processing",
  "message": "Document queued for indexing"
}
```

#### `DELETE /documents/:id` (Admin)

Delete a document and its chunks.

**Response:** `200 OK`

```json
{ "message": "Document and 45 chunks deleted successfully" }
```

---

### Admin

#### `GET /admin/stats`

Get dashboard statistics.

```json
{
  "total_documents": 1247,
  "total_chunks": 28450,
  "total_queries": 8432,
  "total_users": 156,
  "avg_feedback_score": 4.6,
  "avg_response_time_ms": 2100
}
```

#### `GET /admin/analytics/top-questions`

Get most frequently asked questions.

```json
{
  "top_questions": [
    {
      "question": "What is the refund policy?",
      "count": 142,
      "avg_score": 4.8
    },
    { "question": "How do I check PTO balance?", "count": 98, "avg_score": 4.5 }
  ]
}
```

#### `PUT /admin/users/:id/role`

Update a user's role.

| Field  | Type   | Required |
| ------ | ------ | -------- |
| `role` | string | ✅       |

---

## ⚠️ Error Responses

| Code  | Meaning      | Example                  |
| ----- | ------------ | ------------------------ |
| `400` | Bad Request  | Missing required fields  |
| `401` | Unauthorized | Invalid or expired token |
| `403` | Forbidden    | Insufficient permissions |
| `404` | Not Found    | Document not found       |
| `429` | Rate Limited | Too many requests        |
| `500` | Server Error | Internal error           |

```json
{
  "error": "unauthorized",
  "message": "Invalid or expired token",
  "status_code": 401
}
```

---

## 📊 Rate Limits

| Endpoint            | Limit       | Window     |
| ------------------- | ----------- | ---------- |
| `/query`            | 30 requests | Per minute |
| `/documents/upload` | 10 requests | Per minute |
| `/auth/login`       | 5 requests  | Per minute |
| All other endpoints | 60 requests | Per minute |

---

_← [Admin Dashboard](./12-admin-dashboard.md) | [Security →](./14-security.md)_
