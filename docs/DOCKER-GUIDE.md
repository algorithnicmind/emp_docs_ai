# 🐳 Docker Complete Guide — From Zero to Hero

> **A beginner-friendly guide to Docker for the Internal Docs Q&A Agent project**

---

## 🤔 What is Docker?

Think of Docker as a **"box" that contains everything your app needs to run** — code, libraries, databases, settings — all packaged together.

### Real-World Analogy

```
WITHOUT Docker:
  😩 "It works on my machine!"
  😩 "I need to install PostgreSQL, Redis, Python 3.11..."
  😩 "My version is different from yours..."

WITH Docker:
  😎 "Just run: docker compose up"
  😎 Everything works the same everywhere
  😎 No messy installations on your PC
```

### Key Concepts

| Concept            | What It Is                       | Analogy                                          |
| ------------------ | -------------------------------- | ------------------------------------------------ |
| **Image**          | A blueprint/recipe               | Like a cooking recipe 📋                         |
| **Container**      | A running instance of an image   | Like the actual cooked dish 🍕                   |
| **Dockerfile**     | Instructions to build an image   | Like step-by-step cooking instructions           |
| **Docker Compose** | Run multiple containers together | Like a full meal plan (starter + main + dessert) |
| **Volume**         | Persistent storage               | Like a USB drive that survives restarts 💾       |
| **Port Mapping**   | Connect container to your PC     | Like a door between your PC and the container 🚪 |

---

## 📥 Step 1: Install Docker Desktop

### Download

👉 Go to: **https://www.docker.com/products/docker-desktop/**

1. Click **"Download for Windows"**
2. Run the installer (`Docker Desktop Installer.exe`)
3. During installation:
   - ✅ Check "Use WSL 2 instead of Hyper-V" (recommended)
   - ✅ Check "Add shortcut to desktop"
4. Click **Install**
5. **Restart your computer** when prompted

### After Restart

1. Open **Docker Desktop** from your desktop or Start Menu
2. Accept the terms & conditions
3. Wait for Docker to start (you'll see a green "Running" status)
4. Skip the tutorial/sign-in if you want

### Verify Installation

Open PowerShell and run:

```powershell
docker --version
# Expected: Docker version 24.x.x or higher

docker compose version
# Expected: Docker Compose version v2.x.x
```

---

## 🧪 Step 2: Your First Docker Commands (Practice)

Before using Docker for our project, let's learn the basics:

### 2a. Run Your First Container

```powershell
# Pull and run a simple "Hello World" container
docker run hello-world
```

**What happens:**

1. Docker downloads the `hello-world` image (first time only)
2. Creates a container from that image
3. Runs it → prints a success message
4. Container exits

### 2b. Run an Interactive Container

```powershell
# Run Ubuntu Linux inside a container!
docker run -it ubuntu bash
```

**You're now INSIDE a Linux container!** Try:

```bash
whoami          # Shows "root"
cat /etc/os-release   # Shows Ubuntu info
ls              # List files
exit            # Exit the container
```

### 2c. Essential Docker Commands

```powershell
# 📋 List all running containers
docker ps

# 📋 List ALL containers (including stopped)
docker ps -a

# 📋 List all downloaded images
docker images

# 🛑 Stop a running container
docker stop <container_name>

# 🗑️ Remove a stopped container
docker rm <container_name>

# 🗑️ Remove an image
docker rmi <image_name>

# 📊 See container logs
docker logs <container_name>
```

---

## 🗄️ Step 3: Run PostgreSQL with Docker

Now let's run an actual database for our project!

### Option A: Simple One-Line Command

```powershell
docker run -d `
  --name emp-postgres `
  -e POSTGRES_DB=emp_docs_ai `
  -e POSTGRES_USER=postgres `
  -e POSTGRES_PASSWORD=postgres123 `
  -p 5432:5432 `
  -v emp_pgdata:/var/lib/postgresql/data `
  postgres:15-alpine
```

**What each flag means:**

| Flag                       | Meaning                                             |
| -------------------------- | --------------------------------------------------- |
| `-d`                       | Run in background (detached mode)                   |
| `--name emp-postgres`      | Name the container "emp-postgres"                   |
| `-e POSTGRES_DB=...`       | Set environment variable (database name)            |
| `-e POSTGRES_USER=...`     | Set the username                                    |
| `-e POSTGRES_PASSWORD=...` | Set the password                                    |
| `-p 5432:5432`             | Map port 5432 on your PC → port 5432 in container   |
| `-v emp_pgdata:/var/...`   | Save data to a volume (survives container restart!) |
| `postgres:15-alpine`       | Use PostgreSQL 15 (alpine = small size)             |

### Verify PostgreSQL is Running

```powershell
# Check if container is running
docker ps

# Connect to the database from inside the container
docker exec -it emp-postgres psql -U postgres -d emp_docs_ai

# You're now in PostgreSQL! Try:
# \l          (list databases)
# \dt         (list tables - empty for now)
# \q          (quit)
```

---

## 🔴 Step 4: Run Redis with Docker

```powershell
docker run -d `
  --name emp-redis `
  -p 6379:6379 `
  -v emp_redisdata:/data `
  redis:7-alpine
```

### Verify Redis is Running

```powershell
# Check it's running
docker ps

# Test Redis from inside the container
docker exec -it emp-redis redis-cli ping
# Expected output: PONG ✅
```

---

## 🎼 Step 5: Docker Compose (Run Everything Together!)

Instead of running each container separately, **Docker Compose** lets you define everything in one file and start it all with a single command.

### This is the docker-compose.yml we'll use for our project:

```yaml
# This file defines ALL services our project needs
# Start everything with: docker compose up -d
# Stop everything with:  docker compose down

version: "3.8"

services:
  # 🗄️ PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: emp-postgres
    environment:
      POSTGRES_DB: emp_docs_ai
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres123
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    restart: unless-stopped

  # 🔴 Redis Cache
  redis:
    image: redis:7-alpine
    container_name: emp-redis
    ports:
      - "6379:6379"
    volumes:
      - redisdata:/data
    restart: unless-stopped

# 💾 Named volumes (data persists even if containers are removed)
volumes:
  pgdata:
  redisdata:
```

### Docker Compose Commands

```powershell
# 🚀 Start everything (in background)
docker compose up -d

# 📋 See running services
docker compose ps

# 📊 View logs
docker compose logs

# 📊 View logs for specific service
docker compose logs postgres
docker compose logs redis

# 🛑 Stop everything
docker compose down

# 🛑 Stop everything AND delete data
docker compose down -v
```

---

## 📊 Step 6: Useful Docker Desktop GUI Features

After installing Docker Desktop, you can also manage everything visually:

1. **Containers tab** → See running/stopped containers, start/stop them
2. **Images tab** → See downloaded images, delete unused ones
3. **Volumes tab** → See persistent data storage
4. **Logs** → Click any container to see its logs in real-time

---

## 🧹 Step 7: Cleanup Commands

```powershell
# Stop and remove our project containers
docker stop emp-postgres emp-redis
docker rm emp-postgres emp-redis

# Remove ALL stopped containers
docker container prune

# Remove unused images (free up disk space)
docker image prune

# Nuclear option: remove EVERYTHING (containers, images, volumes)
docker system prune -a --volumes
```

---

## 🔧 Common Issues & Fixes

| Problem                       | Solution                                                       |
| ----------------------------- | -------------------------------------------------------------- |
| "Docker Desktop not starting" | Enable WSL 2: Run `wsl --install` in Admin PowerShell, restart |
| "Port 5432 already in use"    | Another PostgreSQL is running. Use `-p 5433:5432` instead      |
| "Permission denied"           | Run PowerShell as Administrator                                |
| "Docker daemon not running"   | Open Docker Desktop app first, wait for green status           |
| "WSL 2 not installed"         | Run `wsl --install` in Admin PowerShell, restart PC            |
| "Slow performance"            | In Docker Desktop Settings → Resources → increase RAM to 4GB   |

---

## 🎯 Quick Reference Cheat Sheet

```
┌─────────────────────────────────────────────────────────┐
│              DOCKER CHEAT SHEET 🐳                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  START:                                                 │
│    docker compose up -d      Start all services         │
│    docker run -d <image>     Run single container       │
│                                                         │
│  CHECK:                                                 │
│    docker ps                 List running containers    │
│    docker compose ps         List compose services      │
│    docker logs <name>        View container logs        │
│                                                         │
│  STOP:                                                  │
│    docker compose down       Stop all services          │
│    docker stop <name>        Stop one container         │
│                                                         │
│  CONNECT:                                               │
│    docker exec -it <name> bash    Open shell inside     │
│    docker exec -it <name> psql    Open PostgreSQL       │
│                                                         │
│  CLEANUP:                                               │
│    docker system prune       Remove unused stuff        │
│    docker compose down -v    Stop + delete data         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

_Happy Dockering! 🐳🚀_
