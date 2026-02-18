"""
Test API Endpoints (Integration-style)
=======================================
Tests the FastAPI routes using httpx TestClient.
Mocks database and external services.

NOTE: These tests require all backend dependencies to be installed.
Run with: pytest tests/test_api.py -v
"""

import pytest

try:
    from fastapi.testclient import TestClient
    from app.main import app
    from app.api.auth import get_current_user
    HAS_DEPS = True
except ImportError as e:
    HAS_DEPS = False
    _import_error = str(e)

skipif_no_deps = pytest.mark.skipif(
    not HAS_DEPS,
    reason=f"Skipping: missing dependency"
)


# ── Mock User ────────────────────────────────────────────────

class MockUser:
    """Mock user object for dependency injection."""
    def __init__(self, role="general", department="general"):
        self.id = "test-user-001"
        self.name = "Test User"
        self.email = "test@company.com"
        self.role = role
        self.department = department
        self.is_active = True


class MockAdminUser(MockUser):
    def __init__(self):
        super().__init__(role="admin", department="all")
        self.id = "test-admin-001"
        self.name = "Admin User"
        self.email = "admin@company.com"


# ── Health Check Tests ───────────────────────────────────────

@skipif_no_deps
class TestHealthEndpoints:
    """Test health and root endpoints (no auth required)."""

    def setup_method(self):
        self.client = TestClient(app)

    def test_root_returns_app_info(self):
        response = self.client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Internal Docs Q&A Agent"
        assert data["status"] == "running"
        assert "version" in data

    def test_health_check(self):
        response = self.client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


# ── Auth Tests ───────────────────────────────────────────────

@skipif_no_deps
class TestAuthEndpoints:
    """Test authentication endpoints."""

    def setup_method(self):
        self.client = TestClient(app)

    def test_login_without_credentials_returns_422(self):
        response = self.client.post("/api/v1/auth/login", data={})
        assert response.status_code == 422

    def test_me_without_token_returns_401(self):
        response = self.client.get("/api/v1/auth/me")
        assert response.status_code == 401

    def test_me_with_valid_user(self):
        """Test /me endpoint with mocked auth."""
        mock_user = MockUser()
        app.dependency_overrides[get_current_user] = lambda: mock_user

        response = self.client.get("/api/v1/auth/me")
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@company.com"
        assert data["role"] == "general"

        app.dependency_overrides.clear()


# ── Query Tests ──────────────────────────────────────────────

@skipif_no_deps
class TestQueryEndpoints:
    """Test query endpoints."""

    def setup_method(self):
        self.client = TestClient(app)

    def test_ask_without_auth_returns_error(self):
        response = self.client.post("/api/v1/query", json={
            "question": "What is the refund policy?"
        })
        assert response.status_code in [401, 403]

    def test_ask_without_question_returns_422(self):
        mock_user = MockUser()
        app.dependency_overrides[get_current_user] = lambda: mock_user

        response = self.client.post("/api/v1/query", json={})
        assert response.status_code == 422

        app.dependency_overrides.clear()


# ── Admin Tests ──────────────────────────────────────────────

@skipif_no_deps
class TestAdminEndpoints:
    """Test admin-only endpoints."""

    def setup_method(self):
        self.client = TestClient(app)

    def test_admin_stats_without_auth_returns_error(self):
        response = self.client.get("/api/v1/admin/stats")
        assert response.status_code in [401, 403]

    def test_admin_stats_with_non_admin_returns_403(self):
        mock_user = MockUser(role="general")
        app.dependency_overrides[get_current_user] = lambda: mock_user

        response = self.client.get("/api/v1/admin/stats")
        assert response.status_code == 403

        app.dependency_overrides.clear()

    def test_admin_users_with_non_admin_returns_403(self):
        mock_user = MockUser(role="engineering")
        app.dependency_overrides[get_current_user] = lambda: mock_user

        response = self.client.get("/api/v1/admin/users")
        assert response.status_code == 403

        app.dependency_overrides.clear()


# ── Document Tests ───────────────────────────────────────────

@skipif_no_deps
class TestDocumentEndpoints:
    """Test document management endpoints."""

    def setup_method(self):
        self.client = TestClient(app)

    def test_documents_without_auth_returns_error(self):
        response = self.client.get("/api/v1/documents")
        assert response.status_code in [401, 403]

    def test_upload_without_auth_returns_error(self):
        response = self.client.post("/api/v1/documents/upload")
        assert response.status_code in [401, 403]
