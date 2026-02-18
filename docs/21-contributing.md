# 🤝 21 — Contributing Guide

> **How to contribute, coding standards, and workflow**

---

## 🚀 Getting Started

### 1. Fork & Clone

```bash
git clone https://github.com/your-username/emp_docs_ai.git
cd emp_docs_ai
```

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 3. Set Up Environment

```bash
python -m venv venv
.\venv\Scripts\activate          # Windows
pip install -r requirements.txt
cp .env.example .env
```

### 4. Make Changes & Test

```bash
pytest --cov=app
```

### 5. Commit & Push

```bash
git add .
git commit -m "feat: add your feature description"
git push origin feature/your-feature-name
```

### 6. Open a Pull Request

- Fill in the PR template
- Link related issues
- Request review from maintainers

---

## 📏 Coding Standards

### Python

- **Style:** Follow PEP 8
- **Type Hints:** Required for functions
- **Docstrings:** Google-style for all public functions
- **Formatting:** Use `black` formatter
- **Linting:** Use `ruff` or `flake8`
- **Imports:** Use `isort` for ordering

```python
# ✅ Good
def process_query(question: str, user_id: str, top_k: int = 5) -> QueryResult:
    """Process a user query and return relevant results.

    Args:
        question: The user's natural language question.
        user_id: The authenticated user's ID.
        top_k: Number of results to return.

    Returns:
        QueryResult with answer and sources.
    """
    ...
```

### JavaScript/TypeScript

- **Style:** ESLint + Prettier
- **Components:** Functional components with hooks
- **Naming:** camelCase for variables, PascalCase for components

---

## 📝 Commit Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat:     New feature
fix:      Bug fix
docs:     Documentation changes
style:    Code style (no logic change)
refactor: Code refactoring
test:     Adding/updating tests
chore:    Maintenance tasks
perf:     Performance improvements
```

**Examples:**

```
feat: add PDF ingestion support
fix: resolve RBAC filtering for HR role
docs: update API reference with new endpoints
test: add unit tests for chunking service
```

---

## 📁 Project Structure Rules

| Directory           | Purpose            | Rules                                  |
| ------------------- | ------------------ | -------------------------------------- |
| `app/models/`       | SQLAlchemy models  | One model per file                     |
| `app/services/`     | Business logic     | Pure functions, testable               |
| `app/api/`          | API route handlers | Thin controllers, delegate to services |
| `app/integrations/` | External APIs      | Abstract behind interfaces             |
| `tests/`            | Test files         | Mirror `app/` structure                |
| `docs/`             | Documentation      | Numbered, markdown format              |

---

## 🔍 Code Review Checklist

- [ ] Code follows project style guidelines
- [ ] All new functions have type hints and docstrings
- [ ] Tests added for new functionality
- [ ] No hardcoded secrets or API keys
- [ ] Error handling is appropriate
- [ ] Changes are documented (if applicable)
- [ ] PR description is clear and complete

---

## 🐛 Reporting Issues

Please include:

1. **Description** — What went wrong?
2. **Steps to Reproduce** — How can we recreate it?
3. **Expected Behavior** — What should happen?
4. **Actual Behavior** — What actually happens?
5. **Screenshots / Logs** — If applicable
6. **Environment** — OS, Python version, etc.

---

_← [Roadmap](./20-roadmap.md) | [Glossary →](./22-glossary.md)_
