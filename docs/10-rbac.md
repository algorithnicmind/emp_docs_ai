# 🔐 10 — Role-Based Access Control (RBAC)

> **Ensuring users only see documents they're authorized to access**

---

## 🎯 Purpose

RBAC ensures that:

- Users can only retrieve documents matching their permission level
- Confidential documents are never leaked to unauthorized users
- Access filtering happens **before** sending context to the LLM

---

## 👥 User Roles

| Role                 | Access Level                     | Description                            |
| -------------------- | -------------------------------- | -------------------------------------- |
| **Admin**            | All documents                    | Full system access, manage users/docs  |
| **HR**               | HR + General + Confidential (HR) | HR policies, employee data             |
| **Engineering**      | Engineering + General            | Technical docs, architecture, runbooks |
| **Finance**          | Finance + General                | Financial policies, budget docs        |
| **General Employee** | General only                     | Company-wide public documents          |

---

## 📄 Document Access Levels

| Access Level   | Who Can Access              | Examples                            |
| -------------- | --------------------------- | ----------------------------------- |
| `all`          | Everyone                    | Company handbook, general policies  |
| `department`   | Specific department + Admin | Engineering runbooks, HR procedures |
| `confidential` | Department leads + Admin    | Salary data, legal docs, M&A info   |

---

## 🔄 Access Control Flow

```
User asks question
      │
      ▼
┌─────────────────────┐
│ 1. Identify User    │  Get user_id from Slack/JWT
│    & Role           │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 2. Retrieve Top-K   │  Get candidates from vector DB
│    Candidates       │  (intentionally fetch more)
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 3. Filter by Access │  Compare user role vs
│    Level            │  chunk access_level metadata
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 4. Send filtered    │  Only authorized chunks
│    context to LLM   │  reach the LLM
└─────────────────────┘
```

---

## 💻 Implementation

```python
class RBACService:
    """Role-Based Access Control for document retrieval."""

    ROLE_PERMISSIONS = {
        "admin": {"all", "department", "confidential"},
        "hr": {"all", "hr_department", "hr_confidential"},
        "engineering": {"all", "eng_department"},
        "finance": {"all", "finance_department"},
        "general": {"all"},
    }

    DEPARTMENT_MAP = {
        "hr": "hr",
        "engineering": "eng",
        "finance": "finance",
    }

    async def get_user_role(self, user_id: str) -> str:
        user = await User.get(user_id)
        return user.role

    def can_access(self, user_role: str, doc_access: str, doc_dept: str) -> bool:
        """Check if a user role can access a document."""
        if user_role == "admin":
            return True
        if doc_access == "all":
            return True
        if doc_access == "department":
            user_dept = self.DEPARTMENT_MAP.get(user_role)
            return user_dept == doc_dept
        if doc_access == "confidential":
            return False  # Only admin can access confidential
        return False

    def filter_results(self, results: list, user_role: str) -> list:
        """Filter search results based on user permissions."""
        return [
            r for r in results
            if self.can_access(user_role, r["access_level"], r["department"])
        ]
```

---

## 🛡️ Security Guarantees

| Guarantee             | Implementation                                  |
| --------------------- | ----------------------------------------------- |
| **Pre-LLM filtering** | Access check happens before context sent to LLM |
| **No data leakage**   | Unauthorized chunks never reach the model       |
| **Audit trail**       | All access attempts are logged                  |
| **Role verification** | Role checked on every query, not cached         |

---

## 📊 Access Control Matrix

| Document Type       | Admin | HR  | Eng | Finance | General |
| ------------------- | :---: | :-: | :-: | :-----: | :-----: |
| Company Handbook    |  ✅   | ✅  | ✅  |   ✅    |   ✅    |
| Engineering Runbook |  ✅   | ❌  | ✅  |   ❌    |   ❌    |
| HR Procedures       |  ✅   | ✅  | ❌  |   ❌    |   ❌    |
| Salary Bands        |  ✅   | ❌  | ❌  |   ❌    |   ❌    |
| Budget Report       |  ✅   | ❌  | ❌  |   ✅    |   ❌    |

---

_← [Interface Layer](./09-interface-layer.md) | [Database Design →](./11-database-design.md)_
