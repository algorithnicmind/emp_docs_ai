# 🛡️ 14 — Security & Compliance

> **Authentication, encryption, and data protection**

---

## 🎯 Security Objectives

1. **Prevent unauthorized access** to documents and data
2. **Encrypt sensitive data** at rest and in transit
3. **Rate limit** API endpoints to prevent abuse
4. **Audit trail** for all access and modifications
5. **Secure integrations** with Slack and external APIs

---

## 🔐 Authentication

### JWT (JSON Web Tokens)

```python
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = os.environ["JWT_SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = verify_token(token)
    user = await User.get(payload["sub"])
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    return user
```

### Slack OAuth 2.0

```
1. Admin clicks "Add to Slack"
2. Redirected to Slack OAuth consent screen
3. User authorizes → Slack sends auth code
4. Server exchanges code for bot token + user token
5. Bot token stored securely for API calls
6. User mapped: slack_id ↔ system user_id
```

---

## 🔒 Encryption

| Layer         | Method   | Details                           |
| ------------- | -------- | --------------------------------- |
| **Transit**   | TLS 1.3  | All HTTP traffic over HTTPS       |
| **At Rest**   | AES-256  | Database encryption               |
| **Passwords** | bcrypt   | Salted hashing, cost factor 12    |
| **API Keys**  | Env Vars | Never hardcoded, stored in `.env` |

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

---

## 🚦 Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/v1/query")
@limiter.limit("30/minute")
async def query_endpoint(request: Request):
    ...

@app.post("/api/v1/auth/login")
@limiter.limit("5/minute")
async def login_endpoint(request: Request):
    ...
```

---

## 🛡️ Security Checklist

| #   | Item                                          | Status    |
| --- | --------------------------------------------- | --------- |
| 1   | JWT authentication on all protected endpoints | ✅        |
| 2   | Password hashing with bcrypt                  | ✅        |
| 3   | HTTPS/TLS in production                       | ✅        |
| 4   | API rate limiting                             | ✅        |
| 5   | CORS configuration                            | ✅        |
| 6   | Input validation/sanitization                 | ✅        |
| 7   | SQL injection prevention (ORM)                | ✅        |
| 8   | XSS prevention                                | ✅        |
| 9   | RBAC access filtering before LLM              | ✅        |
| 10  | Secure Slack OAuth flow                       | ✅        |
| 11  | API keys in environment variables             | ✅        |
| 12  | Audit logging                                 | ✅        |
| 13  | Dependency vulnerability scanning             | 🔜        |
| 14  | SOC 2 compliance                              | 🔜 Future |

---

## 📝 Audit Logging

```python
async def log_access(user_id: str, action: str, resource: str, status: str):
    await AuditLog.create(
        user_id=user_id,
        action=action,        # "query", "upload", "delete", "login"
        resource=resource,    # "document:uuid", "user:uuid"
        status=status,        # "success", "denied", "error"
        ip_address=request.client.host,
        timestamp=datetime.utcnow(),
    )
```

---

## 🌐 CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com", "https://admin.yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

---

## 📋 Environment Variables Security

```bash
# .env.example — NEVER commit actual .env file!
JWT_SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=sk-...
SLACK_BOT_TOKEN=xoxb-...
SLACK_SIGNING_SECRET=...
DATABASE_URL=postgresql://user:pass@host:5432/dbname
REDIS_URL=redis://localhost:6379
```

**`.gitignore` must include:**

```
.env
*.pem
*.key
```

---

_← [API Reference](./13-api-reference.md) | [Performance →](./15-performance.md)_
