# 📈 18 — Evaluation Metrics

> **Measuring system quality, accuracy, and user satisfaction**

---

## 🎯 Why Metrics Matter

RAG systems need continuous evaluation to ensure:

- Answers are **accurate** and based on real documents
- **Hallucinations** are detected and minimized
- Users find responses **helpful**
- System performance stays within **SLAs**

---

## 📊 Core Metrics

### 1. Retrieval Accuracy

**Definition:** How often the correct source documents are retrieved for a query.

```
Retrieval Accuracy = (Relevant chunks retrieved) / (Total chunks retrieved) × 100
```

| Rating     | Score  | Action                    |
| ---------- | ------ | ------------------------- |
| Excellent  | > 90%  | Maintain                  |
| Good       | 80-90% | Monitor                   |
| Needs Work | < 80%  | Tune chunking, embeddings |

### 2. Response Relevance

**Definition:** How well the generated answer addresses the user's question.

Measured via:

- **User feedback** (👍/👎 buttons)
- **Manual evaluation** (sample review)

```
Relevance Score = (Positive feedback) / (Total feedback) × 100

Target: > 85%
```

### 3. Hallucination Rate

**Definition:** Percentage of answers containing information NOT in the source documents.

```
Hallucination Rate = (Answers with unsupported claims) / (Total answers) × 100

Target: < 5%
```

**Detection methods:**

- Compare answer claims against source chunks
- Flag answers where model says "I don't have enough info" but still answers
- Regular manual audits

### 4. Average Response Time

```
Response Time = Query received → Answer delivered

Breakdown:
  Embedding:   ~100ms
  Search:      ~50ms
  RBAC Filter: ~10ms
  LLM Gen:     ~2000ms
  Formatting:  ~50ms
  ─────────────────
  Total:       ~2.2s

Target: < 5 seconds
```

### 5. User Satisfaction (CSAT)

```
CSAT = Average feedback score (1-5 scale)

Target: > 4.5 / 5
```

---

## 📋 Evaluation Framework

### Automated Evaluation Pipeline

```python
class EvaluationPipeline:
    """Automated RAG evaluation."""

    def __init__(self, test_dataset: list):
        self.test_data = test_dataset  # [{question, expected_answer, source_docs}]

    async def evaluate(self) -> dict:
        results = {
            "retrieval_accuracy": [],
            "response_relevance": [],
            "response_time": [],
        }

        for item in self.test_data:
            start = time.time()
            result = await query_pipeline.process(item["question"], user_id="eval")
            elapsed = (time.time() - start) * 1000

            # Retrieval accuracy
            retrieved_docs = set(r.document_id for r in result["sources"])
            expected_docs = set(item["source_docs"])
            accuracy = len(retrieved_docs & expected_docs) / len(expected_docs)

            results["retrieval_accuracy"].append(accuracy)
            results["response_time"].append(elapsed)

        return {
            "avg_retrieval_accuracy": sum(results["retrieval_accuracy"]) / len(results["retrieval_accuracy"]),
            "avg_response_time_ms": sum(results["response_time"]) / len(results["response_time"]),
            "p95_response_time_ms": sorted(results["response_time"])[int(0.95 * len(results["response_time"]))],
        }
```

### Test Dataset Format

```json
[
  {
    "question": "What is the company refund policy?",
    "expected_answer_contains": ["30 days", "original condition", "receipt"],
    "source_docs": ["doc_001"],
    "category": "policy"
  },
  {
    "question": "How do I set up VPN?",
    "expected_answer_contains": [
      "download client",
      "credentials",
      "IT department"
    ],
    "source_docs": ["doc_015"],
    "category": "technical"
  }
]
```

---

## 📊 Dashboard Metrics

| Metric             | Frequency             | Owner   |
| ------------------ | --------------------- | ------- |
| Retrieval Accuracy | Weekly (automated)    | ML Team |
| Response Relevance | Daily (user feedback) | Product |
| Hallucination Rate | Weekly (sampling)     | QA      |
| Response Time      | Real-time             | DevOps  |
| User Satisfaction  | Ongoing               | Product |
| Query Volume       | Real-time             | DevOps  |

---

## 🔄 Continuous Improvement

```
1. Collect feedback → Identify low-scoring queries
2. Analyze failures → Root cause (retrieval? generation? data?)
3. Improve pipeline → Better chunking, new data, prompt tuning
4. Re-evaluate → Run automated test suite
5. Deploy improvements → Monitor impact
```

---

_← [Testing](./17-testing.md) | [Tech Stack →](./19-tech-stack.md)_
