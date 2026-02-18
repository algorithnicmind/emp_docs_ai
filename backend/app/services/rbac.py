"""
RBAC Service — Role-Based Access Control
==========================================
Ensures users only see documents they're authorized to access.
Filtering happens BEFORE context is sent to the LLM.
"""

from typing import List
from loguru import logger


class RBACService:
    """
    Role-Based Access Control for document retrieval.

    Roles:
        - admin:       Access to everything
        - hr:          HR + general documents
        - engineering: Engineering + general documents
        - finance:     Finance + general documents
        - general:     Only public (access_level='all') documents

    Access Levels:
        - all:          Everyone can access
        - department:   Only the owning department + admin
        - confidential: Only admin
    """

    DEPARTMENT_MAP = {
        "hr": "hr",
        "engineering": "engineering",
        "finance": "finance",
    }

    def can_access(
        self, user_role: str, doc_access_level: str, doc_department: str
    ) -> bool:
        """
        Check if a user with the given role can access a document.

        Args:
            user_role: The user's role (admin, hr, engineering, finance, general).
            doc_access_level: The document's access level (all, department, confidential).
            doc_department: The document's owning department.

        Returns:
            True if access is permitted.
        """
        # Admins can access everything
        if user_role == "admin":
            return True

        # Public documents are accessible by everyone
        if doc_access_level == "all":
            return True

        # Department-level: only same department can access
        if doc_access_level == "department":
            user_dept = self.DEPARTMENT_MAP.get(user_role)
            return user_dept is not None and user_dept == doc_department

        # Confidential: only admin (already handled above)
        if doc_access_level == "confidential":
            return False

        # Default deny
        return False

    def filter_results(self, results: List[dict], user_role: str) -> List[dict]:
        """
        Filter search results based on user's access permissions.

        Args:
            results: List of result dicts with 'access_level' and 'department' keys.
            user_role: The user's role.

        Returns:
            Filtered list containing only authorized results.
        """
        filtered = [
            r for r in results
            if self.can_access(
                user_role,
                r.get("access_level", "all"),
                r.get("department", "general"),
            )
        ]

        removed = len(results) - len(filtered)
        if removed > 0:
            logger.info(
                f"RBAC filtered {removed}/{len(results)} results "
                f"for role '{user_role}'"
            )

        return filtered

    def filter_chroma_results(self, results: dict, user_role: str) -> dict:
        """
        Filter ChromaDB query results format based on access permissions.

        Args:
            results: ChromaDB results dict with ids, documents, metadatas, distances.
            user_role: The user's role.

        Returns:
            Filtered ChromaDB results dict.
        """
        if not results or not results.get("ids") or not results["ids"][0]:
            return results

        filtered_indices = []
        for i, metadata in enumerate(results["metadatas"][0]):
            if self.can_access(
                user_role,
                metadata.get("access_level", "all"),
                metadata.get("department", "general"),
            ):
                filtered_indices.append(i)

        return {
            "ids": [[results["ids"][0][i] for i in filtered_indices]],
            "documents": [[results["documents"][0][i] for i in filtered_indices]],
            "metadatas": [[results["metadatas"][0][i] for i in filtered_indices]],
            "distances": [[results["distances"][0][i] for i in filtered_indices]],
        }
