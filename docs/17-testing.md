# 🧪 17 — Testing Strategy

> **Unit, integration, and end-to-end testing approach**

---

## 🎯 Testing Philosophy

| Level                 | Coverage Target  | Tools                       |
| --------------------- | ---------------- | --------------------------- |
| **Unit Tests**        | 80%+             | pytest, unittest.mock       |
| **Integration Tests** | Key flows        | pytest, httpx               |
| **E2E Tests**         | Critical paths   | pytest, Selenium/Playwright |
| **Load Tests**        | Performance SLAs | Locust, k6                  |

---

## 🧩 Unit Tests

### Chunking Service

```python
import pytest
from app.services.chunking import SemanticChunker

class TestSemanticChunker:
    def setup_method(self):
        self.chunker = SemanticChunker(chunk_size=100, overlap=20)

    def test_basic_chunking(self):
        text = "This is paragraph one.\n\nThis is paragraph two.\n\nThis is paragraph three."
        chunks = self.chunker.chunk_document(text, "doc_001")
        assert len(chunks) >= 1
        assert all(c["document_id"] == "doc_001" for c in chunks)

    def test_overlap_exists(self):
        long_text = " ".join(["word"] * 500)
        chunks = self.chunker.chunk_document(long_text, "doc_002")
        if len(chunks) > 1:
            # Check overlap between consecutive chunks
            assert chunks[0]["chunk_text"][-20:] in chunks[1]["chunk_text"][:50]

    def test_empty_input(self):
        chunks = self.chunker.chunk_document("", "doc_003")
        assert len(chunks) == 0

    def test_metadata_preserved(self):
        chunks = self.chunker.chunk_document("Test content", "doc_004")
        assert chunks[0]["chunk_id"].startswith("doc_004")
```

### RBAC Service

```python
class TestRBACService:
    def setup_method(self):
        self.rbac = RBACService()

    def test_admin_access_all(self):
        assert self.rbac.can_access("admin", "confidential", "hr") is True

    def test_general_no_confidential(self):
        assert self.rbac.can_access("general", "confidential", "hr") is False

    def test_department_access(self):
        assert self.rbac.can_access("engineering", "department", "eng") is True
        assert self.rbac.can_access("engineering", "department", "hr") is False

    def test_all_access_for_everyone(self):
        for role in ["admin", "hr", "engineering", "finance", "general"]:
            assert self.rbac.can_access(role, "all", "any") is True
```

---

## 🔗 Integration Tests

### API Endpoints

```python
import httpx
import pytest

@pytest.fixture
def client():
    return httpx.AsyncClient(app=app, base_url="http://test")

@pytest.mark.asyncio
async def test_query_endpoint(client, auth_headers):
    response = await client.post("/api/v1/query", json={
        "question": "What is the refund policy?"
    }, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data

@pytest.mark.asyncio
async def test_upload_document(client, admin_headers, sample_pdf):
    response = await client.post("/api/v1/documents/upload",
        files={"file": sample_pdf},
        data={"title": "Test Doc", "department": "general"},
        headers=admin_headers
    )
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_unauthorized_access(client):
    response = await client.post("/api/v1/query", json={
        "question": "test"
    })
    assert response.status_code == 401
```

---

## 📊 Test Data

```python
# tests/fixtures.py
SAMPLE_DOCUMENTS = [
    {
        "title": "Company Handbook",
        "text": "Our company values include integrity, innovation...",
        "department": "general",
        "access_level": "all",
    },
    {
        "title": "Engineering Standards",
        "text": "All code must pass code review before merging...",
        "department": "engineering",
        "access_level": "department",
    },
]
```

---

## ▶️ Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_chunking.py -v

# Run only unit tests
pytest tests/unit/ -v

# Run integration tests
pytest tests/integration/ -v
```

---

## 📈 CI/CD Pipeline

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: test_db
          POSTGRES_PASSWORD: test
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pytest --cov=app --cov-report=xml
      - uses: codecov/codecov-action@v3
```

---

_← [Deployment](./16-deployment.md) | [Evaluation Metrics →](./18-evaluation-metrics.md)_
