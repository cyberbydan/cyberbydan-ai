# CyberByDan AI Architecture

> System architecture for the CyberByDan AI Platform.

---

# Overview

CyberByDan AI is a self-hosted Retrieval-Augmented Generation (RAG) platform designed to provide a single OpenAI-compatible interface for local AI applications.

The platform combines local language models, a vector database, and custom retrieval logic behind a persistent REST API.

---

# High-Level Architecture

```text
                        Clients
────────────────────────────────────────────────────

Open WebUI
Continue
n8n
Telegram Bot (Future)
WhatsApp Bot (Future)
Custom Applications

                    │
                    ▼

             CyberByDan AI API
          (FastAPI / Windows Service)

                    │
      ┌─────────────┴─────────────┐
      │                           │
      ▼                           ▼

 Retriever                 Ollama API
      │                           │
      ▼                           ▼

 ChromaDB                Local LLMs

      │

 Stored Knowledge
```

---

# Platform Components

## CyberByDan AI API

Responsibilities

* OpenAI-compatible REST API
* Request validation
* Context generation
* Prompt construction
* Response formatting

Runs as

* Windows Service
* Managed by NSSM
* Automatic startup

Monitoring

* Managed through the CyberByDan AI PowerShell Toolkit
* Health verification via ai-health.ps1
* Status reporting via ai-status.ps1
* Centralized logs in C:\homelab\logs

---

## Ollama

Responsibilities

* Local model inference
* Embedding generation

Current Models

* CyberByDan-AI
* deepseek-r1:14b
* qwen2.5-coder:14b
* qwen2.5-coder
* mistral
* llama3.2
* nomic-embed-text

---

## ChromaDB

Responsibilities

* Vector storage
* Similarity search
* Document retrieval

Deployment

* Podman Compose
* Dedicated AI stack

---

## Retriever

Responsibilities

* Query embedding
* Similarity search
* Context retrieval
* Chunk selection

Future

* Cross-encoder reranking
* Hybrid search
* Metadata filtering

---

# Request Flow

```text
User Request

      │

      ▼

OpenAI API

      │

      ▼

Retriever

      │

      ▼

ChromaDB

      │

      ▼

Relevant Chunks

      │

      ▼

Prompt Builder

      │

      ▼

DeepSeek

      │

      ▼

OpenAI-Compatible Response
```

---

# Startup Architecture

```text
Windows Boot

      │

      ▼

Podman Machine

      │

      ▼

Media Compose Stack

      │

      ▼

AI Compose Stack

      │

      ▼

ChromaDB

      │

      ▼

Ollama

      │

      ▼

CyberByDanAI Windows Service

      │

      ▼

Clients
```

---

# Directory Structure

```text
C:\homelab\ai

├── api/
├── chat/
├── chromadb/
├── ingest/
├── models/
├── prompts/
├── vectorstore/
├── docs/
├── scripts/
└── tests/
```

---

# Infrastructure

## Windows

* CyberByDanAI Service
* NSSM
* PowerShell Toolkit

---

## Podman

AI Stack

* ChromaDB

Media Stack

* Sonarr
* Radarr
* Lidarr
* Bazarr
* Prowlarr
* Jellyseerr
* qBittorrent
* FlareSolverr
* Navidrome

---

# Management Toolkit

PowerShell scripts provide lifecycle management.

Available commands

* ai-start.ps1
* ai-stop.ps1
* ai-restart.ps1
* ai-status.ps1
* ai-health.ps1
* ai-update.ps1

Shared Library

* ai-common.ps1

---

# Logging

Application

```text
C:\homelab\logs\api.log
```

Errors

```text
C:\homelab\logs\api-error.log
```

---

# Design Principles

* Local-first AI
* OpenAI compatibility
* Modular components
* Service-oriented architecture
* Separation of infrastructure and application logic
* Automation-friendly operations
* Persistent services
* Reproducible deployments

---

# Current Architecture Status

Implemented

* OpenAI-compatible API
* Windows Service hosting
* Automatic startup
* Podman-managed ChromaDB
* Ollama integration
* Retrieval-Augmented Generation
* PowerShell management toolkit
* Health monitoring
* Structured logging

Planned

* Cross-encoder reranker
* Conversation memory
* Agent framework
* MCP integration
* Multi-user authentication
* Observability dashboards
* Distributed inference
* Multi-vector retrieval

---

# Operational Status

The CyberByDan AI Platform currently provides:

* Automatic startup after Windows reboot
* Persistent Windows service hosting via NSSM
* Podman-managed ChromaDB deployment
* OpenAI-compatible API
* Retrieval-Augmented Generation (RAG)
* Local DeepSeek reasoning
* Ollama model hosting
* Unified AI management toolkit
* Health monitoring and diagnostics
* Structured application logging
* Production-ready local AI foundation

Current platform maturity:

Production-ready core platform with ongoing feature development.
