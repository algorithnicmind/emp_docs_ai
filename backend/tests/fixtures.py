"""
Test Fixtures
==============
Shared test data, fixtures, and helpers for all test suites.
"""

import pytest
from unittest.mock import MagicMock, AsyncMock


# ── Sample Users ─────────────────────────────────────────────

ADMIN_USER = {
    "id": "user-admin-001",
    "name": "Admin User",
    "email": "admin@company.com",
    "role": "admin",
    "department": "all",
    "is_active": True,
}

HR_USER = {
    "id": "user-hr-001",
    "name": "HR Manager",
    "email": "hr@company.com",
    "role": "hr",
    "department": "hr",
    "is_active": True,
}

ENG_USER = {
    "id": "user-eng-001",
    "name": "Engineer",
    "email": "eng@company.com",
    "role": "engineering",
    "department": "engineering",
    "is_active": True,
}

GENERAL_USER = {
    "id": "user-gen-001",
    "name": "General Employee",
    "email": "employee@company.com",
    "role": "general",
    "department": "general",
    "is_active": True,
}


# ── Sample Documents ────────────────────────────────────────

SAMPLE_DOCUMENTS = [
    {
        "title": "Company Handbook 2024",
        "text": (
            "Our company values include integrity, innovation, and teamwork. "
            "All employees are expected to follow the code of conduct. "
            "The standard work week is Monday to Friday, 9 AM to 5 PM. "
            "Remote work is available for eligible positions with manager approval. "
            "Annual performance reviews are conducted in Q4."
        ),
        "department": "general",
        "access_level": "all",
        "source": "handbook",
    },
    {
        "title": "Engineering Standards",
        "text": (
            "All code must pass code review before merging to main branch. "
            "Use semantic versioning for releases. Write unit tests for all "
            "new features with minimum 80% coverage. Use TypeScript for "
            "frontend and Python for backend services."
        ),
        "department": "engineering",
        "access_level": "department",
        "source": "engineering_wiki",
    },
    {
        "title": "HR Salary Bands",
        "text": (
            "Salary bands are structured by level: L1 $50k-$70k, "
            "L2 $70k-$90k, L3 $90k-$120k, L4 $120k-$160k, "
            "L5 $160k-$220k. Annual raises are 3-8% based on performance. "
            "Equity grants vest over 4 years with a 1-year cliff."
        ),
        "department": "hr",
        "access_level": "confidential",
        "source": "hr_portal",
    },
    {
        "title": "Refund Policy",
        "text": (
            "Customers may request a full refund within 30 days of purchase. "
            "After 30 days, a prorated refund is available for annual plans. "
            "To process a refund, submit a ticket via the support portal. "
            "Refunds are processed within 5-7 business days."
        ),
        "department": "general",
        "access_level": "all",
        "source": "support_docs",
    },
    {
        "title": "Finance Budget Q1",
        "text": (
            "Q1 2024 budget allocation: Engineering $2.5M, Marketing $1.2M, "
            "Sales $800K, Operations $600K. Cloud infrastructure costs are "
            "projected at $150K/month. All expenditures over $10K require "
            "VP approval."
        ),
        "department": "finance",
        "access_level": "department",
        "source": "finance_docs",
    },
]


# ── ChromaDB-style Mock Results ─────────────────────────────

MOCK_CHROMA_RESULTS = {
    "ids": [["chunk_1", "chunk_2", "chunk_3"]],
    "documents": [[
        "Our refund policy allows returns within 30 days.",
        "All code must pass code review before merging.",
        "Annual performance reviews are conducted in Q4.",
    ]],
    "metadatas": [[
        {
            "document_id": "doc-001",
            "title": "Refund Policy",
            "source": "support_docs",
            "department": "general",
            "access_level": "all",
        },
        {
            "document_id": "doc-002",
            "title": "Engineering Standards",
            "source": "engineering_wiki",
            "department": "engineering",
            "access_level": "department",
        },
        {
            "document_id": "doc-003",
            "title": "Company Handbook",
            "source": "handbook",
            "department": "general",
            "access_level": "all",
        },
    ]],
    "distances": [[0.15, 0.32, 0.45]],
}

MOCK_EMPTY_RESULTS = {
    "ids": [[]],
    "documents": [[]],
    "metadatas": [[]],
    "distances": [[]],
}
