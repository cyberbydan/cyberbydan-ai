# CyberByDan AI Architecture

## Vision

CyberByDan AI separates the responsibilities of document ingestion, retrieval, prompt engineering and language model inference into independent modules.

Each component performs one responsibility.

---

## High-Level Architecture

```
Knowledge Sources
        │
        ▼
Discover Documents
        │
        ▼
Read Documents
        │
        ▼
Chunk Documents
        │
        ▼
Generate Embeddings
        │
        ▼
Store in ChromaDB
        │
        ▼
Retrieve Relevant Chunks
        │
        ▼
Context Builder
        │
        ▼
Prompt Builder
        │
        ▼
Language Model
        │
        ▼
OpenAI API
        │
        ▼
Clients
```

---

## Components

### Knowledge Sources

Defines every documentation source available to the AI.

Configured in

```
core/config.py
```

---

### Ingestion

Responsible for

- discovery
- reading
- chunking
- embeddings

---

### ChromaDB

Stores semantic vectors.

Responsibilities

- storage

- retrieval

- similarity search

---

### Retriever

Performs semantic search.

Returns the most relevant chunks.

---

### Context Builder

Converts retrieved chunks into structured context.

---

### Prompt Builder

Combines

- system instructions
- context
- user question

into one prompt.

---

### Language Model

DeepSeek-R1 running through Ollama.

---

### OpenAI API

Exposes the AI using the OpenAI Chat Completion API.

---

## Future Architecture

- Re-ranking
- Memory
- Agent framework
- Tool calling
- Infrastructure awareness
- Autonomous planning
