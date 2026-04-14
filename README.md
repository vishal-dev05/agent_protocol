# 🤖 Autonomous AI Agent Protocol

A lightweight **Agent Platform** built with FastAPI where AI agents can register, discover each other, call each other, and track usage — with built-in idempotency, validation, and NLP-powered search.

---

## 🚀 Quick Start

```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

Open Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📁 Project Structure

```
project/
├── main.py       # FastAPI app — all route handlers
├── models.py     # Pydantic data models (Agent, Usage)
├── storage.py    # In-memory storage layer
└── README.md     # Documentation
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/agents` | Register a new agent |
| `GET` | `/agents` | List all registered agents |
| `GET` | `/search?q=...` | Search agents by keyword |
| `POST` | `/usage` | Log a usage event between agents |
| `GET` | `/usage-summary` | Get total units consumed per agent |
| `GET` | `/usage-logs` | View all raw usage logs |

---

## 🧪 Example Usage

### Register an Agent
```json
POST /agents
{
  "name": "SummariserAgent",
  "description": "Summarises long documents using NLP techniques",
  "endpoint": "http://localhost:8002/summarise",
  "tags": []
}
```

### Log Usage Between Agents
```json
POST /usage
{
  "caller": "OrchestratorAgent",
  "target": "SummariserAgent",
  "units": 150,
  "request_id": "req-001"
}
```

---

## 🛡️ Edge Cases Handled

| Scenario | Behaviour |
|----------|-----------|
| Duplicate agent name | `400` error — agent already exists |
| Unknown caller/target | `400` error — agent not found |
| Duplicate `request_id` | Silently ignored (idempotent) |
| Missing/invalid fields | Auto-handled by Pydantic (`422` error) |

---

## ⚙️ Design Decisions

**Idempotency**
Duplicate `request_id` values are silently ignored to prevent double billing. In production, this set would be stored in Redis for persistence across restarts.

**Validation**
Pydantic models enforce field types and constraints automatically — no manual checks needed.

**NLP Tag Extraction**
When registering an agent, keywords are auto-extracted from the description by filtering stopwords. This improves search accuracy.

**Scalability Path**
The storage layer is fully abstracted in `storage.py`. To scale:
- Replace `agents` dict → PostgreSQL with indexed columns
- Replace `usage_logs` list → TimescaleDB or append-only table
- Replace `request_ids` set → Redis SET for O(1) deduplication

---

## 📈 Scaling to 100K+ Agents

- **Database**: Move to PostgreSQL with indexes on `name` and `description`
- **Search**: Use Elasticsearch for full-text search with relevance scoring
- **Caching**: Cache frequent searches in Redis (60s TTL)
- **Architecture**: Split into microservices — Registry, Search, Usage as separate services
- **Async Logging**: Use Kafka/RabbitMQ to decouple usage logging from the hot path

---

## 🧰 Tech Stack

- **Python 3.11**
- **FastAPI** — modern async web framework
- **Pydantic** — data validation
- **Uvicorn** — ASGI server
