# 💬 09 — Interface Layer

> **Slack Integration & Web Chat UI**

---

## 🎯 Purpose

The Interface Layer provides the user-facing endpoints through which employees interact with the Q&A Agent:

- **Slack Bot** — Primary interface for teams using Slack
- **Web Chat UI** — Browser-based alternative

---

## 💬 Slack Integration

### Architecture

```
┌──────────────────────────────────────────┐
│              SLACK WORKSPACE              │
│                                          │
│  User types: /ask What is the PTO policy?│
│       │                                  │
│       ▼                                  │
│  Slack API sends event to our server     │
└──────────────┬───────────────────────────┘
               │ HTTPS POST
               ▼
┌──────────────────────────────────────────┐
│           OUR BACKEND                     │
│  ┌─────────────────────────┐             │
│  │  Slack Event Handler     │             │
│  │  • Verify signature      │             │
│  │  • Parse command          │             │
│  │  • Identify user          │             │
│  └────────────┬────────────┘             │
│               ▼                          │
│  ┌─────────────────────────┐             │
│  │  Query Pipeline          │             │
│  │  • Embed → Search → LLM  │             │
│  └────────────┬────────────┘             │
│               ▼                          │
│  ┌─────────────────────────┐             │
│  │  Response Formatter      │             │
│  │  • Slack Block Kit       │             │
│  │  • Add citations         │             │
│  │  • Add feedback buttons  │             │
│  └────────────┬────────────┘             │
└───────────────┼──────────────────────────┘
                │ Slack API POST
                ▼
┌──────────────────────────────────────────┐
│         SLACK THREAD REPLY               │
│  🤖 Bot: "Based on our HR policy..."    │
│  📎 Sources: [HR Handbook p.12]         │
│  👍 👎 Was this helpful?                │
└──────────────────────────────────────────┘
```

### Slack Bot Setup

```python
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler

app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
)

@app.command("/ask")
async def handle_ask(ack, command, say):
    """Handle /ask slash command."""
    await ack("🔍 Searching company docs...")

    user_id = command["user_id"]
    question = command["text"]

    # Process query through RAG pipeline
    result = await query_pipeline.process(
        question=question, slack_user_id=user_id
    )

    # Format response with Slack Block Kit
    blocks = format_slack_response(result)
    await say(blocks=blocks, thread_ts=command.get("thread_ts"))

@app.action("feedback_helpful")
async def handle_feedback(ack, body, action):
    """Handle feedback button clicks."""
    await ack()
    query_id = action["value"]
    await log_feedback(query_id, score=1)

@app.action("feedback_not_helpful")
async def handle_negative_feedback(ack, body, action):
    await ack()
    query_id = action["value"]
    await log_feedback(query_id, score=-1)
```

### Slack Response Format (Block Kit)

```python
def format_slack_response(result) -> list:
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Answer:*\n{result['answer']}"
            }
        },
        {"type": "divider"},
        {
            "type": "context",
            "elements": [
                {"type": "mrkdwn",
                 "text": f"📎 *Sources:* {', '.join(result['sources'])}"}
            ]
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "👍 Helpful"},
                    "action_id": "feedback_helpful",
                    "value": result["query_id"]
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "👎 Not Helpful"},
                    "action_id": "feedback_not_helpful",
                    "value": result["query_id"]
                }
            ]
        }
    ]
    return blocks
```

---

## 🌐 Web Chat UI

### User Flow

```
1. User logs in (JWT auth)
2. Types question in chat interface
3. System processes query through RAG pipeline
4. Response streams back in real-time
5. Sources displayed as clickable links
6. User can rate response quality
```

### API Endpoint

```python
@router.post("/api/query")
async def web_query(
    request: QueryRequest,
    current_user: User = Depends(get_current_user)
):
    result = await query_pipeline.process(
        question=request.question,
        user_id=current_user.id
    )
    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "query_id": result["query_id"],
    }

@router.post("/api/query/stream")
async def web_query_stream(
    request: QueryRequest,
    current_user: User = Depends(get_current_user)
):
    """Stream response using Server-Sent Events."""
    async def event_stream():
        async for token in query_pipeline.process_stream(
            question=request.question, user_id=current_user.id
        ):
            yield f"data: {json.dumps({'token': token})}\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")
```

---

## 🔐 Slack OAuth Flow

```
1. Admin installs app → Slack OAuth redirect
2. User authorizes → Receive access token
3. Store token → Map Slack user_id to system user
4. Bot joins channels → Ready to respond
```

---

## 📱 Supported Commands

| Command        | Description          | Example                        |
| -------------- | -------------------- | ------------------------------ |
| `/ask`         | Ask a question       | `/ask What is the PTO policy?` |
| `/ask-sources` | List indexed sources | `/ask-sources`                 |
| `/ask-help`    | Show help message    | `/ask-help`                    |

---

_← [LLM Generation](./08-llm-generation.md) | [RBAC →](./10-rbac.md)_
