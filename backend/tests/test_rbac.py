"""
Test RBAC Service
==================
Unit tests for role-based access control logic.
"""

import pytest
from app.services.rbac import RBACService


class TestRBACService:
    """Test the RBAC filtering logic."""

    def setup_method(self):
        self.rbac = RBACService()

    # ── Admin Access ─────────────────────────────────────────

    def test_admin_can_access_all_docs(self):
        assert self.rbac.can_access("admin", "all", "general") is True

    def test_admin_can_access_department_docs(self):
        assert self.rbac.can_access("admin", "department", "hr") is True

    def test_admin_can_access_confidential_docs(self):
        assert self.rbac.can_access("admin", "confidential", "hr") is True

    # ── Department Access ────────────────────────────────────

    def test_hr_can_access_public_docs(self):
        assert self.rbac.can_access("hr", "all", "general") is True

    def test_hr_can_access_hr_department_docs(self):
        assert self.rbac.can_access("hr", "department", "hr") is True

    def test_hr_cannot_access_engineering_docs(self):
        assert self.rbac.can_access("hr", "department", "engineering") is False

    def test_hr_cannot_access_confidential_docs(self):
        assert self.rbac.can_access("hr", "confidential", "hr") is False

    def test_engineering_can_access_own_department(self):
        assert self.rbac.can_access("engineering", "department", "engineering") is True

    def test_engineering_cannot_access_hr_docs(self):
        assert self.rbac.can_access("engineering", "department", "hr") is False

    # ── General Employee Access ──────────────────────────────

    def test_general_can_access_public_docs(self):
        assert self.rbac.can_access("general", "all", "general") is True

    def test_general_cannot_access_department_docs(self):
        assert self.rbac.can_access("general", "department", "hr") is False

    def test_general_cannot_access_confidential_docs(self):
        assert self.rbac.can_access("general", "confidential", "general") is False

    # ── Filtering ────────────────────────────────────────────

    def test_filter_results_removes_unauthorized(self):
        results = [
            {"access_level": "all", "department": "general", "text": "public"},
            {"access_level": "department", "department": "hr", "text": "hr-only"},
            {"access_level": "confidential", "department": "hr", "text": "secret"},
        ]

        filtered = self.rbac.filter_results(results, "general")
        assert len(filtered) == 1
        assert filtered[0]["text"] == "public"

    def test_filter_results_admin_sees_all(self):
        results = [
            {"access_level": "all", "department": "general"},
            {"access_level": "department", "department": "hr"},
            {"access_level": "confidential", "department": "hr"},
        ]

        filtered = self.rbac.filter_results(results, "admin")
        assert len(filtered) == 3

    def test_filter_chroma_results(self):
        results = {
            "ids": [["id1", "id2", "id3"]],
            "documents": [["doc1", "doc2", "doc3"]],
            "metadatas": [[
                {"access_level": "all", "department": "general"},
                {"access_level": "department", "department": "hr"},
                {"access_level": "confidential", "department": "hr"},
            ]],
            "distances": [[0.1, 0.2, 0.3]],
        }

        filtered = self.rbac.filter_chroma_results(results, "general")
        assert len(filtered["ids"][0]) == 1
        assert filtered["ids"][0][0] == "id1"
