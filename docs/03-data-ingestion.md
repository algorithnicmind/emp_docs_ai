# 📥 03 — Data Ingestion Layer

> **Collecting and normalizing documents from multiple sources**

---

## 🎯 Purpose

The Data Ingestion Layer is responsible for:

- Connecting to various document sources
- Extracting raw text and metadata
- Normalizing data into a unified format
- Triggering downstream processing (chunking → embedding → storage)

---

## 📂 Supported Sources

### Source Matrix

| Source             | Type        | API                 | Auth Method | Status     |
| ------------------ | ----------- | ------------------- | ----------- | ---------- |
| **PDF Upload**     | File        | Direct Upload       | JWT         | ✅ MVP     |
| **Markdown Files** | File        | Direct Upload       | JWT         | ✅ MVP     |
| **Notion**         | API         | Notion API v1       | OAuth 2.0   | 🔜 Phase 2 |
| **Google Docs**    | API         | Google Drive API v3 | OAuth 2.0   | 🔜 Phase 2 |
| **Confluence**     | API         | Confluence REST API | API Token   | 🔜 Phase 2 |
| **Shared Drives**  | File System | OS/Network          | Server Auth | 🔜 Phase 3 |
| **Plain Text**     | File        | Direct Upload       | JWT         | ✅ MVP     |

---

## 📄 PDF Ingestion

### Process Flow

```
PDF File Upload
    │
    ▼
┌────────────────────┐
│  PDF Parser         │
│  (PyPDF2 / pdfplumber)│
│                     │
│  • Extract text     │
│  • Preserve layout  │
│  • Handle tables    │
│  • Extract images   │
│    (OCR if needed)  │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  Metadata Extractor │
│                     │
│  • Title (from      │
│    filename/header) │
│  • Page count       │
│  • Author (if avail)│
│  • Created date     │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  Normalized Output  │
│  (UnifiedDocument)  │
└────────────────────┘
```

### Code Example

```python
from pdfplumber import open as pdf_open

class PDFIngester:
    """Ingests PDF documents and extracts text + metadata."""

    def ingest(self, file_path: str, metadata: dict) -> dict:
        text = ""
        with pdf_open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        return {
            "raw_text": text,
            "metadata": {
                "title": metadata.get("title", file_path.stem),
                "source": "pdf_upload",
                "author": metadata.get("author", "Unknown"),
                "department": metadata.get("department", "General"),
                "access_level": metadata.get("access_level", "all"),
                "page_count": len(pdf.pages),
                "file_size": file_path.stat().st_size,
                "source_url": None,
                "uploaded_at": datetime.utcnow().isoformat(),
            }
        }
```

---

## 📝 Markdown Ingestion

### Process Flow

```
Markdown File Upload
    │
    ▼
┌────────────────────┐
│  MD Parser          │
│  (markdown-it /     │
│   python-markdown)  │
│                     │
│  • Parse headings   │
│  • Extract text     │
│  • Remove formatting│
│  • Preserve         │
│    structure hints  │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  Normalized Output  │
│  (UnifiedDocument)  │
└────────────────────┘
```

---

## 🔗 Notion API Integration (Phase 2)

### Connection Setup

```python
from notion_client import Client

class NotionIngester:
    def __init__(self, token: str):
        self.client = Client(auth=token)

    def fetch_database(self, database_id: str) -> list:
        """Fetch all pages from a Notion database."""
        results = []
        response = self.client.databases.query(database_id=database_id)

        for page in response["results"]:
            page_content = self._get_page_content(page["id"])
            results.append({
                "raw_text": page_content,
                "metadata": {
                    "title": self._extract_title(page),
                    "source": "notion",
                    "source_url": page["url"],
                    "last_edited": page["last_edited_time"],
                    "created_by": page["created_by"]["id"],
                }
            })

        return results

    def _get_page_content(self, page_id: str) -> str:
        """Extract all text blocks from a Notion page."""
        blocks = self.client.blocks.children.list(block_id=page_id)
        text_parts = []

        for block in blocks["results"]:
            block_type = block["type"]
            if block_type in ["paragraph", "heading_1", "heading_2",
                              "heading_3", "bulleted_list_item",
                              "numbered_list_item"]:
                rich_texts = block[block_type].get("rich_text", [])
                text = "".join([rt["plain_text"] for rt in rich_texts])
                text_parts.append(text)

        return "\n".join(text_parts)
```

---

## 📊 Google Docs Integration (Phase 2)

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

class GoogleDocsIngester:
    def __init__(self, credentials_path: str):
        creds = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=["https://www.googleapis.com/auth/documents.readonly"]
        )
        self.service = build("docs", "v1", credentials=creds)

    def fetch_document(self, doc_id: str) -> dict:
        """Fetch a Google Doc by ID."""
        doc = self.service.documents().get(documentId=doc_id).execute()

        text = self._extract_text(doc.get("body", {}).get("content", []))

        return {
            "raw_text": text,
            "metadata": {
                "title": doc.get("title", "Untitled"),
                "source": "google_docs",
                "source_url": f"https://docs.google.com/document/d/{doc_id}",
                "last_modified": doc.get("revisionId"),
            }
        }
```

---

## 🌐 Confluence Integration (Phase 2)

```python
from atlassian import Confluence

class ConfluenceIngester:
    def __init__(self, url: str, username: str, api_token: str):
        self.client = Confluence(url=url, username=username, password=api_token)

    def fetch_space(self, space_key: str) -> list:
        """Fetch all pages from a Confluence space."""
        pages = self.client.get_all_pages_from_space(
            space_key, start=0, limit=100,
            expand="body.storage"
        )

        results = []
        for page in pages:
            html_content = page["body"]["storage"]["value"]
            text = self._html_to_text(html_content)

            results.append({
                "raw_text": text,
                "metadata": {
                    "title": page["title"],
                    "source": "confluence",
                    "source_url": page["_links"]["webui"],
                    "space": space_key,
                }
            })

        return results
```

---

## 📋 Extracted Data Schema

Every ingested document is normalized into a **UnifiedDocument** format:

```python
@dataclass
class UnifiedDocument:
    """Standardized document representation after ingestion."""

    raw_text: str              # Full extracted text
    metadata: DocumentMetadata  # Structured metadata

@dataclass
class DocumentMetadata:
    title: str                 # Document title
    author: str                # Author name or ID
    department: str            # Owning department (HR, Eng, Finance, etc.)
    access_level: str          # "all", "department", "confidential"
    source: str                # "pdf_upload", "notion", "gdocs", "confluence"
    source_url: Optional[str]  # Original document URL
    created_at: datetime       # When document was created
    updated_at: datetime       # Last modification time
    tags: List[str]            # Custom tags for categorization
    file_type: str             # "pdf", "md", "html", "txt"
    page_count: Optional[int]  # Number of pages (PDFs)
    word_count: int            # Total word count
```

---

## 🔄 Sync Strategies

### Strategy Comparison

| Strategy           | Trigger      | Latency   | Complexity | Use Case          |
| ------------------ | ------------ | --------- | ---------- | ----------------- |
| **Manual Upload**  | User action  | Immediate | Low        | MVP / Small teams |
| **Scheduled Sync** | Cron job     | Hours     | Medium     | Regular updates   |
| **Webhook**        | Source event | Real-time | High       | Enterprise        |

### Manual Upload

```python
@router.post("/documents/upload")
async def upload_document(
    file: UploadFile,
    title: str = Form(...),
    department: str = Form(...),
    access_level: str = Form("all"),
    current_user: User = Depends(get_current_user)
):
    """Upload and ingest a document manually."""
    # 1. Save file
    file_path = await save_upload(file)

    # 2. Ingest
    ingester = get_ingester(file.content_type)
    document = ingester.ingest(file_path, {
        "title": title,
        "department": department,
        "access_level": access_level,
        "author": current_user.name,
    })

    # 3. Trigger processing pipeline
    await process_document(document)

    return {"status": "success", "document_id": document.id}
```

### Scheduled Sync

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

@scheduler.scheduled_job("interval", hours=6)
async def scheduled_sync():
    """Sync documents from all connected sources every 6 hours."""
    sources = await get_active_sources()

    for source in sources:
        try:
            ingester = get_ingester_for_source(source)
            new_docs = await ingester.fetch_updates(since=source.last_sync)

            for doc in new_docs:
                await process_document(doc)

            source.last_sync = datetime.utcnow()
            await source.save()

            logger.info(f"Synced {len(new_docs)} docs from {source.name}")
        except Exception as e:
            logger.error(f"Sync failed for {source.name}: {e}")
```

### Webhook-Based Sync

```python
@router.post("/webhooks/notion")
async def notion_webhook(payload: dict):
    """Handle Notion update webhook."""
    page_id = payload.get("page_id")
    event_type = payload.get("event")  # "page.updated", "page.created"

    if event_type in ["page.updated", "page.created"]:
        ingester = NotionIngester(settings.NOTION_TOKEN)
        document = await ingester.fetch_page(page_id)
        await process_document(document, upsert=True)

    elif event_type == "page.deleted":
        await delete_document_by_source("notion", page_id)

    return {"status": "ok"}
```

---

## ⚠️ Error Handling

| Error Type      | Handling Strategy                       |
| --------------- | --------------------------------------- |
| API Rate Limit  | Exponential backoff with retry          |
| Auth Failure    | Alert admin, disable source temporarily |
| Parse Error     | Log error, skip document, notify admin  |
| Network Timeout | Retry with configurable timeout         |
| Corrupt File    | Log error, skip, notify uploader        |

---

## 📊 Ingestion Metrics

Tracked metrics for monitoring:

| Metric                       | Description                           |
| ---------------------------- | ------------------------------------- |
| `docs_ingested_total`        | Total documents successfully ingested |
| `docs_failed_total`          | Total ingestion failures              |
| `ingestion_duration_seconds` | Time taken per document               |
| `source_sync_last_success`   | Last successful sync timestamp        |
| `docs_pending_processing`    | Queue size for processing             |

---

_← [System Architecture](./02-system-architecture.md) | [Text Processing & Chunking →](./04-text-processing.md)_
