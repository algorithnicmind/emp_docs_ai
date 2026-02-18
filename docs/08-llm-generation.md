# 🤖 08 — LLM Generation Layer

> **Generating accurate, citation-backed answers using GPT-4**

---

## 🎯 Purpose

The LLM Generation Layer takes the assembled context from the Query Processing Layer and generates a human-readable, accurate answer with source citations.

---

## 🔄 Generation Pipeline

```
┌──────────────────────────────────────┐
│           INPUTS                     │
│  • System instruction                │
│  • Retrieved context (Top-K chunks)  │
│  • User question                     │
│  • Citation format requirements      │
└──────────────┬───────────────────────┘
               ▼
┌──────────────────────────────────────┐
│         PROMPT CONSTRUCTION          │
│  Combine all inputs into structured  │
│  prompt with clear instructions      │
└──────────────┬───────────────────────┘
               ▼
┌──────────────────────────────────────┐
│         LLM GENERATION               │
│  GPT-4 / GPT-4-turbo                │
│  Temperature: 0.1 (factual)          │
└──────────────┬───────────────────────┘
               ▼
┌──────────────────────────────────────┐
│        POST-PROCESSING               │
│  • Format citations                  │
│  • Validate answer quality           │
│  • Add confidence indicator          │
└──────────────────────────────────────┘
```

---

## 📝 Prompt Template

```python
SYSTEM_PROMPT = """You are an internal company knowledge assistant.
Your job is to answer employee questions using ONLY the provided context.

RULES:
1. Answer ONLY based on the provided context
2. If the context doesn't contain enough information, say so
3. Always cite your sources using [Source N] format
4. Be concise but thorough
5. Never make up information not in the context
6. If multiple sources agree, synthesize the answer
"""

def build_prompt(context: str, question: str) -> list:
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"""
CONTEXT:
{context}

QUESTION: {question}

Provide a clear answer with source citations [Source N].
"""}
    ]
```

---

## 💻 Implementation

```python
import openai

class LLMGenerator:
    """Generate answers using retrieved context."""

    def __init__(self, model: str = "gpt-4"):
        self.client = openai.OpenAI()
        self.model = model

    async def generate(self, context: str, question: str) -> dict:
        messages = build_prompt(context, question)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1,
            max_tokens=1000,
        )

        answer = response.choices[0].message.content
        usage = response.usage

        return {
            "answer": answer,
            "model": self.model,
            "tokens_used": {
                "prompt": usage.prompt_tokens,
                "completion": usage.completion_tokens,
                "total": usage.total_tokens,
            },
        }

    async def generate_stream(self, context: str, question: str):
        """Streaming response for real-time delivery."""
        messages = build_prompt(context, question)
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1,
            max_tokens=1000,
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
```

---

## 📋 Response Format

```json
{
  "answer": "The refund policy allows returns within 30 days of purchase [Source 1]. Enterprise customers have an extended 60-day window [Source 2].",
  "sources": [
    {
      "index": 1,
      "title": "General Refund Policy",
      "source": "pdf_upload",
      "document_id": "doc_001"
    },
    {
      "index": 2,
      "title": "Enterprise Customer Agreement",
      "source": "confluence",
      "document_id": "doc_042"
    }
  ],
  "confidence": "high",
  "tokens_used": 847
}
```

---

## ⚙️ LLM Configuration

| Parameter     | Value | Rationale                       |
| ------------- | ----- | ------------------------------- |
| `model`       | gpt-4 | Best accuracy for factual Q&A   |
| `temperature` | 0.1   | Low creativity, high accuracy   |
| `max_tokens`  | 1000  | Sufficient for detailed answers |
| `top_p`       | 1.0   | Default nucleus sampling        |

---

## 🛡️ Guardrails

- **No Context = No Answer:** If no relevant chunks found, respond with "I don't have enough information."
- **Hallucination Prevention:** Low temperature + strict system prompt
- **Token Budget:** Cap total context + response under model limit
- **Content Filter:** Block inappropriate or off-topic responses

---

_← [Query Processing](./07-query-processing.md) | [Interface Layer →](./09-interface-layer.md)_
