<div align="center">
  <img src="https://images.unsplash.com/photo-1677442136019-21780ecad995?q=80&w=2832&auto=format&fit=crop" width="100%" height="300px" style="object-fit: cover; border-radius: 10px;" alt="Banner">

  <h1 style="font-size: 3rem; margin-top: 20px;">🧠 Internal Docs Q&A Agent</h1>

  <p style="font-size: 1.2rem; max-width: 600px;">
    <strong>Unlock your company's knowledge with an AI-powered, RAG-based assistant.</strong><br>
    Instantly answer questions, cite sources, and enforce detailed access controls.
  </p>

  <p>
    <a href="#-key-features">✨ Features</a> •
    <a href="#-tech-stack">🛠️ Tech Stack</a> •
    <a href="#-getting-started">🚀 Getting Started</a> •
    <a href="#-documentation">📚 Documentation</a>
  </p>

  <div style="margin-top: 20px;">
    <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/FastAPI-0.109+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
    <img src="https://img.shields.io/badge/React-18.0+-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React">
    <img src="https://img.shields.io/badge/OpenAI-GPT--4-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI">
    <img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
    <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
  </div>
</div>

<br>

---

## 🌟 Overview

The **Internal Docs Q&A Agent** is an enterprise-ready solution designed to aggregate scattered internal documentation (PDFs, Markdown, Text) into a unified, searchable knowledge base. It uses **Retrieval-Augmented Generation (RAG)** to provide accurate, context-aware answers to employee queries while strictly adhering to **Role-Based Access Control (RBAC)**.

Whether you are in HR, Engineering, or Finance, the agent ensures you only see information you are authorized to access.

---

## ✨ Key Features

| Feature                       | Description                                                                           |
| :---------------------------- | :------------------------------------------------------------------------------------ |
| **🤖 Advanced RAG Engine**    | Uses vector similarity search (ChromaDB) + GPT-4 to generate citation-backed answers. |
| **🔐 Granular RBAC**          | Restrict document access by department (HR, Engineering) and clearance level.         |
| **📄 Multi-Format Ingestion** | Seamlessly parses and indexes **PDFs**, **Markdown**, and **Text** files.             |
| **⚡ Real-Time Streaming**    | Typewriter-style token streaming for a responsive user experience.                    |
| **📊 Admin Dashboard**        | Track usage, view query analytics, and manage document lifecycles.                    |
| **🧠 Mock Mode**              | Built-in simulation mode to test the full pipeline _without_ API keys.                |

---

## 🛠️ Tech Stack

### **Backend**

- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL (Metadata), ChromaDB (Vectors), Redis (Caching)
- **Auth**: OAuth2 with JWT
- **AI**: OpenAI API (Embeddings + ChatCompletion), LangChain

### **Frontend**

- **Framework**: Next.js 14 (React)
- **Styling**: Tailwind CSS
- **State**: Context API + Axios
- **Icons**: Lucide React

---

## 🏗️ Architecture

```mermaid
graph TD
    User[User] -->|Query| FE[Frontend (Next.js)]
    FE -->|API Call| BE[Backend (FastAPI)]

    subgraph "RAG Pipeline"
        BE -->|Embed Query| OpenAI[OpenAI API]
        BE -->|Search Stats| DB[(PostgreSQL)]
        BE -->|Vector Search| Chroma[(ChromaDB)]
        Chroma -->|Top K Chunks| BE
        BE -->|Assemble Context| OpenAI
        OpenAI -->|Generated Answer| BE
    end

    BE -->|Stream Response| FE
    FE -->|Display| User
```

---

## 🚀 Getting Started

Follow these steps to set up the project locally.

### 1️⃣ Clone & Configure

```bash
git clone https://github.com/your-org/emp_docs_ai.git
cd emp_docs_ai

# Setup Environment Variables
cp .env.example .env
# (Optional) Edit .env to add OPENAI_API_KEY
```

### 2️⃣ Start Backend with Docker

```bash
docker-compose up -d postgres redis
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 3️⃣ Start Frontend

```bash
cd frontend
npm install
npm run dev
```

> **Note:** The application will run at `http://localhost:3000`. The API is available at `http://localhost:8000`.

---

## 📸 Screenshots

|                                                                       Login Interface                                                                        |                                                                        Admin Dashboard                                                                        |
| :----------------------------------------------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------------------------------: |
| <img src="https://images.unsplash.com/photo-1481487484168-9b93081dfdcd?q=80&w=2600&auto=format&fit=crop" width="100%" style="border-radius:6px" alt="Login"> | <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=2600&auto=format&fit=crop" width="100%" style="border-radius:6px" alt="Dashboard"> |

---

## 📂 Project Structure

```bash
emp_docs_ai/
├── 📂 backend/             # FastAPI Application
│   ├── 📂 app/             # Application Logic
│   │   ├── 📂 api/         # Routes (Auth, Query, Admin)
│   │   ├── 📂 services/    # Business Logic (RAG, Ingestion)
│   │   └── 📂 models/      # SQLAlchemy Models
│   └── 📄 requirements.txt # Python Dependencies
│
├── 📂 frontend/            # Next.js Application
│   ├── 📂 src/             # Source Code
│   │   ├── 📂 app/         # Pages & Layouts
│   │   └── 📂 components/  # Reusable UI Components
│   └── 📄 package.json     # Node Dependencies
│
└── 📄 docker-compose.yml   # Infrastructure Setup
```

---

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

<div align="center">
  <p>Built with ❤️ by the AI Engineering Team</p>
</div>
