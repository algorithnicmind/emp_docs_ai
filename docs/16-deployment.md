# 🚀 16 — Deployment Guide

> **Local setup, Docker, and cloud deployment**

---

## 📋 Prerequisites

| Tool       | Version | Purpose             |
| ---------- | ------- | ------------------- |
| Python     | 3.10+   | Backend runtime     |
| Node.js    | 18+     | Frontend build      |
| PostgreSQL | 15+     | Relational database |
| Redis      | 7+      | Caching layer       |
| Docker     | 24+     | Containerization    |
| Git        | 2.30+   | Version control     |

---

## 🖥️ Local Development Setup

### Step 1: Clone Repository

```bash
git clone https://github.com/your-org/emp_docs_ai.git
cd emp_docs_ai
```

### Step 2: Backend Setup

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your API keys:

```env
# Application
APP_ENV=development
APP_PORT=8000
DEBUG=true

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/emp_docs_ai

# Redis
REDIS_URL=redis://localhost:6379

# OpenAI
OPENAI_API_KEY=sk-your-key-here

# JWT
JWT_SECRET_KEY=your-super-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60

# Slack
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_SIGNING_SECRET=your-signing-secret
SLACK_APP_TOKEN=xapp-your-app-token

# Vector Store
VECTOR_STORE_PATH=./vector_store
VECTOR_STORE_TYPE=chroma
```

### Step 4: Database Setup

```bash
# Create database
createdb emp_docs_ai

# Run migrations
alembic upgrade head

# Seed initial data (optional)
python scripts/seed_data.py
```

### Step 5: Run Development Server

```bash
# Backend
uvicorn app.main:app --reload --port 8000

# Frontend (in another terminal)
cd frontend
npm install
npm run dev
```

---

## 🐳 Docker Deployment

### docker-compose.yml

```yaml
version: "3.8"

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/emp_docs_ai
      - REDIS_URL=redis://redis:6379
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
    depends_on:
      - db
      - redis
    volumes:
      - vector_data:/app/vector_store

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: emp_docs_ai
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  worker:
    build: ./backend
    command: celery -A app.worker worker --loglevel=info
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/emp_docs_ai
      - REDIS_URL=redis://redis:6379

volumes:
  postgres_data:
  redis_data:
  vector_data:
```

### Backend Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Run with Docker

```bash
# Build and start all services
docker-compose up --build -d

# View logs
docker-compose logs -f backend

# Stop all services
docker-compose down
```

---

## ☁️ Cloud Deployment Options

| Provider    | Service        | Best For                |
| ----------- | -------------- | ----------------------- |
| **Railway** | PaaS           | Quick deploy, free tier |
| **Render**  | PaaS           | Easy Docker deploy      |
| **AWS**     | ECS / Lambda   | Production scale        |
| **GCP**     | Cloud Run      | Serverless              |
| **Azure**   | Container Apps | Enterprise              |

---

## ✅ Deployment Checklist

- [ ] Set all environment variables in production
- [ ] Enable HTTPS/TLS
- [ ] Set `DEBUG=false`
- [ ] Configure CORS for production domains
- [ ] Set up database backups
- [ ] Configure monitoring (Sentry, etc.)
- [ ] Set up CI/CD pipeline
- [ ] Load test the application
- [ ] Review security checklist

---

_← [Performance](./15-performance.md) | [Testing Strategy →](./17-testing.md)_
