# CyberByDan AI API

> OpenAI-compatible REST API for interacting with CyberByDan AI.

---

# Overview

CyberByDan AI exposes an OpenAI-compatible API so that existing
applications can communicate with the local AI without modification.

Current supported clients include:

- Open WebUI
- Continue
- n8n
- Custom Python applications
- REST clients
- Future Telegram Bot
- Future WhatsApp integration

The API currently supports chat completions and dynamic model
discovery.

---

# Base URL

Local

```
http://localhost:8001
```

Example

```
http://localhost:8001/v1
```

---

# Authentication

Currently

```
No authentication
```

Future versions will support

- API Keys
- JWT
- Authentik
- Role-based access

---

# API Compatibility

CyberByDan follows the OpenAI Chat Completions API.

Supported endpoints

| Endpoint                  | Status |
| ------------------------- | ------ |
| GET /v1/models            | ✅      |
| POST /v1/chat/completions | ✅      |

Planned

| Endpoint            | Status  |
| ------------------- | ------- |
| GET /v1/health      | Planned |
| GET /v1/version     | Planned |
| POST /v1/embeddings | Planned |
| POST /v1/rerank     | Planned |

---

# Endpoint

## GET /v1/models

Returns every model available to clients.

CyberByDan AI appears first.

Local Ollama models are appended automatically.

Example Request

```http
GET /v1/models
```

Example Response

```json
{
  "object": "list",
  "data": [
    {
      "id": "CyberByDan-AI",
      "object": "model",
      "owned_by": "CyberByDan"
    },
    {
      "id": "deepseek-r1:14b",
      "object": "model",
      "owned_by": "Ollama"
    }
  ]
}
```

---

# Endpoint

## POST /v1/chat/completions

Primary endpoint used by Open WebUI and compatible clients.

Workflow

```
Question

↓

Retriever

↓

Context Builder

↓

Prompt Builder

↓

DeepSeek

↓

OpenAI Response
```

---

## Request

```http
POST /v1/chat/completions
Content-Type: application/json
```

Example

```json
{
  "model": "CyberByDan-AI",
  "messages": [
    {
      "role": "user",
      "content": "Explain my homelab architecture."
    }
  ]
}
```

---

## Response

```json
{
  "id": "response-id",
  "object": "chat.completion",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "..."
      },
      "finish_reason": "stop"
    }
  ]
}
```

---

# Internal Processing Pipeline

Every request follows this sequence.

```
Receive Request
        │
        ▼
Retrieve Relevant Chunks
        │
        ▼
Re-rank (future)
        │
        ▼
Build Context
        │
        ▼
Build Prompt
        │
        ▼
Generate Response
        │
        ▼
Return OpenAI-Compatible JSON
```

---

# Model Routing

CyberByDan AI

```
User

↓

CyberByDan API

↓

Retriever

↓

DeepSeek
```

Local Ollama Models

```
User

↓

Open WebUI

↓

Ollama

↓

Selected Model
```

CyberByDan AI currently uses

```
deepseek-r1:14b
```

as its reasoning model.

---

# Error Handling

Current responses

| Code | Meaning               |
| ---- | --------------------- |
| 200  | Success               |
| 500  | Internal server error |

Future

| Code | Meaning                 |
| ---- | ----------------------- |
| 400  | Invalid request         |
| 401  | Authentication required |
| 404  | Resource not found      |
| 429  | Rate limit exceeded     |

---

# Planned Endpoints

## GET /v1/health

Returns

- API status
- Chroma status
- Ollama status
- Loaded model
- Uptime

---

## GET /v1/version

Returns

- API version
- Git commit
- Build date
- Model version

---

## POST /v1/embeddings

Generate embeddings through the configured embedding model.

---

## POST /v1/rerank

Cross-encoder endpoint for future retrieval improvements.

---

# Design Philosophy

CyberByDan AI separates the AI platform from the user interface.

Every client communicates through the same OpenAI-compatible API.

This allows improvements to retrieval, prompting, memory and reasoning
to benefit every connected application without requiring client-side
changes.
