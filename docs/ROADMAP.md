# CyberByDan AI Roadmap

> Living roadmap for the CyberByDan AI platform.
>
> Last Updated:
> Owner: Dan Isaaka
> Status: Active Development

---

# Vision

CyberByDan AI is not simply a chatbot.

It is a personal AI operating system capable of understanding,
reasoning over, monitoring and controlling my entire homelab.

Long-term goals include:

- RAG over all documentation
- Infrastructure awareness
- Long-term memory
- Agent workflows
- Telegram assistant
- WhatsApp assistant
- OpenAI-compatible API
- Observability
- Secure remote administration
- Autonomous task execution

---

# Current Architecture

Current pipeline

Knowledge Sources
        │
        ▼
Discovery
        │
        ▼
Reader
        │
        ▼
Chunker
        │
        ▼
Embedding
        │
        ▼
ChromaDB
        │
        ▼
Retriever
        │
        ▼
Context Builder
        │
        ▼
Prompt Builder
        │
        ▼
DeepSeek
        │
        ▼
OpenAI API
        │
        ▼
Open WebUI

Current Status

✅ Working

---

# Development Roadmap

---

## Phase 1 — Foundation

Goal

Build a reliable RAG system.

Status

Mostly Complete

Tasks

- [x] Project structure
- [x] ChromaDB integration
- [x] Embedding pipeline
- [x] Chunking
- [x] Markdown splitting
- [x] Knowledge source abstraction
- [x] OpenAI API
- [x] Open WebUI integration
- [x] Context Builder
- [x] Prompt Builder
- [x] Retriever
- [x] Semantic search
- [ ] Automatic API service
- [ ] Health endpoint
- [ ] Logging improvements

---

## Phase 2 — Better Retrieval

Goal

Improve answer quality before adding more features.

Status

In Progress

Tasks

- [ ] Cross encoder reranker
- [ ] Similarity threshold filtering
- [ ] Metadata boosting
- [ ] Filename weighting
- [ ] Section weighting
- [ ] Duplicate chunk removal
- [ ] Context compression
- [ ] Source citations
- [ ] Token counting
- [ ] Prompt optimisation

Deliverable

CyberByDan answers should consistently outperform raw DeepSeek on homelab questions.

---

## Phase 3 — Memory

Goal

Remember previous conversations.

Status

Planned

Features

Short-term memory

- recent conversation

Working memory

- current objective
- current sprint

Long-term memory

- preferences
- architecture decisions
- lessons learned
- recurring tasks

Future

Memory summarisation

Memory pruning

Memory importance scoring

Memory retrieval

---

## Phase 4 — Infrastructure Awareness

Goal

Understand the state of the homelab.

Features

- Docker status
- Podman status
- Services
- CPU
- RAM
- GPU
- Disk
- Network
- UPS
- Temperature
- Internet status

Future

Live topology graph

---

## Phase 5 — Control Plane

Goal

Take safe actions.

Examples

Restart services

Run backups

Restore backups

Update containers

Search logs

Check health

Restart Jellyfin

Restart n8n

Restart Chroma

Safe approval workflow before dangerous actions.

---

## Phase 6 — Multi-Agent System

Agents

Infrastructure Engineer

Documentation Assistant

Media Assistant

DevOps Assistant

Security Analyst

Software Developer

Research Agent

Future

Planner Agent

Executor Agent

Reviewer Agent

---

## Phase 7 — Integrations

Telegram

- monitoring
- notifications
- commands

WhatsApp

Discord

Slack

Email

GitHub

Jira

Home Assistant

---

## Phase 8 — AI Engineering

Goal

Become production-grade.

Tasks

- [ ] Unit tests
- [ ] Integration tests
- [ ] Benchmark retrieval
- [ ] Benchmark prompts
- [ ] Prompt versioning
- [ ] Evaluation datasets
- [ ] Latency monitoring
- [ ] Token accounting
- [ ] Automatic regression testing

---

## Phase 9 — Observability

Metrics

Response latency

Embedding latency

Retrieval latency

Generation latency

Context size

Prompt size

Tokens

GPU utilisation

Memory usage

API requests

Errors

---

## Phase 10 — Release

CyberByDan AI v1

Features

- Production API
- Production documentation
- Installer
- Docker deployment
- Podman deployment
- Automatic updates
- Authentication
- Web dashboard

---

# Technical Debt

Current known issues

- [ ] API currently started manually
- [ ] No automatic service installation
- [ ] Retrieval still distance-only
- [ ] No reranker
- [ ] No source citations
- [ ] No prompt evaluation suite
- [ ] No memory subsystem
- [ ] No streaming responses
- [ ] No caching
- [ ] No conversation persistence

---

# Sprint Backlog

Current Sprint

Improve retrieval quality.

Tasks

- [ ] Add reranker
- [ ] Improve prompt
- [ ] Improve retrieval scoring
- [ ] Add citations
- [ ] Build API service
- [ ] Test from phone
- [ ] Test through Tailscale

---

# Future Ideas

Things worth exploring

- MCP integration
- Local code interpreter
- Multi-modal support
- Vision
- Speech
- Voice assistant
- Calendar agent
- Personal knowledge graph
- GraphRAG
- Neo4j
- Hybrid search
- BM25 + embeddings
- Cross encoder reranking
- Reflection loops
- Agentic planning
- Tool calling
- Local function calling
- Automatic documentation updates

---

# Definition of Done

A feature is considered complete when:

- Code implemented
- Documentation updated
- Tested
- Added to architecture docs
- Added to roadmap
- Commit pushed
- Demonstrated in Open WebUI
