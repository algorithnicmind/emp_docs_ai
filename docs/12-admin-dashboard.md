# 📊 12 — Admin Dashboard

> **Centralized management for documents, users, and analytics**

---

## 🎯 Purpose

The Admin Dashboard provides a web-based interface for system administrators to:

- Upload and manage documents
- Monitor system health and usage
- Manage users and roles
- View query analytics and identify knowledge gaps

---

## 🖥️ Dashboard Features

### 1. Overview / Home

```
┌────────────────────────────────────────────────────────────┐
│  📊 ADMIN DASHBOARD                              [Logout] │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌─────────┐│
│  │ 📄 1,247   │ │ 🔍 8,432  │ │ 👥 156     │ │ ⭐ 4.6   ││
│  │ Documents  │ │ Queries    │ │ Users      │ │ Rating   ││
│  │ Indexed    │ │ This Month │ │ Active     │ │ Avg.     ││
│  └────────────┘ └────────────┘ └────────────┘ └─────────┘│
│                                                            │
│  ┌─────────────────────────────┐ ┌────────────────────────┐│
│  │ 📈 Query Volume (30 days)  │ │ 🏆 Top Questions       ││
│  │                             │ │                        ││
│  │  ▁▂▃▄▅▆▇█▇▆▅▆▇█▇▆▅       │ │ 1. Refund policy (142) ││
│  │                             │ │ 2. PTO balance (98)    ││
│  │                             │ │ 3. VPN setup (87)      ││
│  │                             │ │ 4. Expense report (76) ││
│  └─────────────────────────────┘ └────────────────────────┘│
└────────────────────────────────────────────────────────────┘
```

### 2. Document Management

| Feature             | Description                                 |
| ------------------- | ------------------------------------------- |
| **Upload**          | Upload PDF, Markdown, or plain text files   |
| **Sync Sources**    | Connect Notion, Google Docs, Confluence     |
| **View Index**      | See all indexed documents with metadata     |
| **Delete/Update**   | Remove or re-index documents                |
| **Status Tracking** | Monitor processing, indexed, or failed docs |

### 3. User Management

| Feature           | Description                              |
| ----------------- | ---------------------------------------- |
| **View Users**    | List all registered users with roles     |
| **Assign Roles**  | Change user roles (Admin, HR, Eng, etc.) |
| **Slack Mapping** | Link Slack user IDs to system accounts   |
| **Deactivate**    | Disable user access without deletion     |

### 4. Query Analytics

| Feature                 | Description                                |
| ----------------------- | ------------------------------------------ |
| **Top Questions**       | Most frequently asked questions            |
| **Unanswered Queries**  | Questions with low confidence / no results |
| **Response Quality**    | Average feedback scores over time          |
| **Usage by Department** | Which teams use the bot most               |
| **Response Times**      | Average and P95 response latency           |

### 5. System Health

| Metric             | Description                    |
| ------------------ | ------------------------------ |
| **Vector DB Size** | Total chunks / vectors stored  |
| **API Latency**    | Average query processing time  |
| **Error Rate**     | Failed queries percentage      |
| **Sync Status**    | Last sync time per data source |

---

## 🔌 Admin API Endpoints

```
GET    /api/v1/admin/stats              → Dashboard statistics
GET    /api/v1/documents                → List all documents
POST   /api/v1/documents/upload         → Upload new document
DELETE /api/v1/documents/:id            → Delete a document
POST   /api/v1/documents/:id/reindex    → Re-index a document (Future)
GET    /api/v1/admin/users              → List all users
PUT    /api/v1/admin/users/:id/role     → Update user role
GET    /api/v1/admin/analytics/queries  → Query analytics (recent)
GET    /api/v1/admin/analytics/top      → Top questions
GET    /api/v1/admin/sources            → List data sources (Future)
POST   /api/v1/admin/sources/sync       → Trigger manual sync (Future)
GET    /api/v1/admin/health             → System health check (Use /health)
```

---

## 🔐 Admin Authorization

Only users with `role = "admin"` can access the dashboard:

```python
def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user
```

---

_← [Database Design](./11-database-design.md) | [API Reference →](./13-api-reference.md)_
