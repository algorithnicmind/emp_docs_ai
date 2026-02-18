# 🚀 Installation & Setup Guide

> **Step-by-step guide to set up the Internal Docs Q&A Agent**

---

## 📋 Prerequisites Checklist

Before you begin, install these tools on your system:

### ✅ Required

| #   | Tool        | Version | Download                                                  | Check Command      |
| --- | ----------- | ------- | --------------------------------------------------------- | ------------------ |
| 1   | **Python**  | 3.11+   | [python.org/downloads](https://www.python.org/downloads/) | `python --version` |
| 2   | **pip**     | Latest  | Comes with Python                                         | `pip --version`    |
| 3   | **Node.js** | 18+     | [nodejs.org](https://nodejs.org/)                         | `node --version`   |
| 4   | **Git**     | 2.30+   | [git-scm.com](https://git-scm.com/)                       | `git --version`    |

### 💡 Recommended

| #   | Tool               | Why                           | Download                                                      |
| --- | ------------------ | ----------------------------- | ------------------------------------------------------------- |
| 5   | **Docker Desktop** | Run PostgreSQL + Redis easily | [docker.com](https://www.docker.com/products/docker-desktop/) |
| 6   | **VS Code**        | Best editor for this project  | [code.visualstudio.com](https://code.visualstudio.com/)       |
| 7   | **Postman**        | Test API endpoints            | [postman.com](https://www.postman.com/downloads/)             |
| 8   | **pgAdmin**        | PostgreSQL GUI                | [pgadmin.org](https://www.pgadmin.org/download/)              |

### 🔑 API Keys Needed

| Service    | What For           | Sign Up                                                              |
| ---------- | ------------------ | -------------------------------------------------------------------- |
| **OpenAI** | GPT-4 + Embeddings | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) |
| **Slack**  | Bot integration    | [api.slack.com/apps](https://api.slack.com/apps)                     |

---

## 🛠️ Installation Steps

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-org/emp_docs_ai.git
cd emp_docs_ai
```

### Step 2: Create Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate it (Windows CMD)
.\venv\Scripts\activate.bat

# Activate it (macOS/Linux)
source venv/bin/activate
```

> You should see `(venv)` at the beginning of your terminal prompt.

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs **all** the packages listed below:

| Category           | Key Packages                              |
| ------------------ | ----------------------------------------- |
| **Web Framework**  | FastAPI, Uvicorn, Pydantic                |
| **Database**       | SQLAlchemy, Alembic, asyncpg              |
| **AI/ML**          | OpenAI, tiktoken, LangChain               |
| **Vector DB**      | ChromaDB, FAISS                           |
| **Doc Processing** | pdfplumber, PyPDF2, python-docx, markdown |
| **Auth**           | python-jose (JWT), passlib (bcrypt)       |
| **Slack**          | slack-bolt, slack-sdk                     |
| **Caching**        | Redis, Celery                             |
| **Utils**          | python-dotenv, loguru, httpx              |
| **Testing**        | pytest, pytest-asyncio, pytest-cov        |

### Step 4: Set Up Environment Variables

```bash
# Copy the example env file
copy .env.example .env

# Now edit .env and add your actual API keys:
# - OPENAI_API_KEY (required!)
# - DATABASE_URL
# - SLACK_BOT_TOKEN (for Slack integration)
```

### Step 5: Set Up PostgreSQL Database

#### Option A: Using Docker (Recommended)

```bash
# Start PostgreSQL + Redis with Docker
docker run -d --name emp-postgres \
  -e POSTGRES_DB=emp_docs_ai \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=your_password \
  -p 5432:5432 \
  postgres:15-alpine

docker run -d --name emp-redis \
  -p 6379:6379 \
  redis:7-alpine
```

#### Option B: Local PostgreSQL Install

1. Download from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Install with default settings
3. Create database:

```sql
CREATE DATABASE emp_docs_ai;
```

### Step 6: Run Database Migrations

```bash
# Initialize Alembic (first time only)
alembic init alembic

# Generate migration
alembic revision --autogenerate -m "initial tables"

# Apply migration
alembic upgrade head
```

### Step 7: Create Vector Store Directory

```bash
mkdir vector_store
```

### Step 8: Run the Application

```bash
# Start the backend server
uvicorn app.main:app --reload --port 8000

# The API will be available at:
# http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Step 9: Set Up Frontend (Admin Dashboard)

```bash
cd frontend
npm install
npm run dev

# Frontend available at: http://localhost:3000
```

---

## 🧪 Verify Installation

Run these commands to verify everything is working:

```bash
# Check Python
python --version          # Should show 3.11+

# Check packages installed
pip list | findstr fastapi    # Should show fastapi
pip list | findstr openai     # Should show openai
pip list | findstr chromadb   # Should show chromadb

# Check Node.js
node --version            # Should show 18+

# Check Docker (if using)
docker --version          # Should show 24+

# Run tests
pytest --version          # Should show pytest 8+
```

---

## ⚡ Quick Start (After Installation)

```bash
# 1. Activate venv
.\venv\Scripts\Activate.ps1

# 2. Start backend
uvicorn app.main:app --reload --port 8000

# 3. Open API docs
# Go to http://localhost:8000/docs

# 4. Upload a test PDF
# Use the /documents/upload endpoint

# 5. Ask a question
# POST to /query with {"question": "your question here"}
```

---

## 🐛 Common Issues

### "pip not recognized"

→ Add Python to your PATH during installation, or use `python -m pip` instead.

### "Module not found" errors

→ Make sure your virtual environment is activated: `.\venv\Scripts\Activate.ps1`

### PostgreSQL connection refused

→ Check if PostgreSQL is running: `docker ps` or check Windows Services

### OpenAI API errors

→ Verify your `OPENAI_API_KEY` in `.env` is valid and has credits

### ChromaDB import errors

→ Try: `pip install chromadb --upgrade`

### FAISS installation fails on Windows

→ Use: `pip install faiss-cpu` (not `faiss-gpu`)

---

## 📦 VS Code Extensions (Recommended)

| Extension              | Purpose                      |
| ---------------------- | ---------------------------- |
| **Python** (Microsoft) | Python language support      |
| **Pylance**            | Type checking & IntelliSense |
| **Python Debugger**    | Debugging support            |
| **REST Client**        | Test API endpoints           |
| **Docker**             | Docker container management  |
| **PostgreSQL**         | Database explorer            |
| **Markdown Preview**   | Preview docs                 |
| **GitLens**            | Git history & blame          |

---

_For full documentation, see the [docs/](./docs/) folder._
