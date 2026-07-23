# CyberByDan AI API

## Overview

The CyberByDan AI API provides an OpenAI-compatible REST interface for interacting with the local AI platform. It acts as a compatibility layer between external applications and the local inference engine powered by Ollama and ChromaDB.

The API is designed to be a permanent infrastructure service rather than a development-only application.

---

# Architecture

```text
Client
    │
    ▼
CyberByDan AI API
    │
    ├── Ollama
    │      └── Local LLMs
    │
    └── ChromaDB
           └── Retrieval-Augmented Generation (RAG)
```

---

# Service Information

**Service Name**

```text
CyberByDanAI
```

**Service Manager**

```text
NSSM (Non-Sucking Service Manager)
```

**Startup Type**

```text
Automatic
```

The API starts automatically during Windows boot and remains available without requiring an active PowerShell or VS Code session.

---

# Endpoints

## Base URL

```text
http://127.0.0.1:8001
```

---

## OpenAI Compatible API

### List Models

```http
GET /v1/models
```

Returns all locally available chat and embedding models.

---

### Chat Completions

```http
POST /v1/chat/completions
```

OpenAI-compatible endpoint for conversational requests.

Supported by:

* Open WebUI
* n8n
* Telegram Bots
* WhatsApp Bots
* Custom Applications
* Future CyberByDan Clients

---

## Health Endpoints

### API Health

```http
GET /
```

Returns a simple API status response.

---

# Dependencies

The API depends on the following infrastructure services:

## Ollama

Purpose

* Local LLM inference
* Embedding generation

Default Endpoint

```text
http://127.0.0.1:11434
```

---

## ChromaDB

Purpose

* Vector database
* Document retrieval
* RAG context storage

Default Endpoint

```text
http://127.0.0.1:8000
```

---

# Startup Process

Windows Boot

↓

Podman Machine

↓

AI Infrastructure (ChromaDB)

↓

CyberByDanAI Windows Service

↓

API Ready

The API assumes that required infrastructure services are available before processing requests.

---

# Logging

Standard Output

```text
C:\homelab\logs\api.log
```

Standard Error

```text
C:\homelab\logs\api-error.log
```

Logs are managed automatically by NSSM.

---

# Management Scripts

The API lifecycle is managed using the PowerShell toolkit.

Available commands:

```text
ai-start.ps1
ai-stop.ps1
ai-restart.ps1
ai-status.ps1
ai-health.ps1
ai-update.ps1
```

These scripts should be used instead of manually launching Uvicorn.

---

# Configuration

Primary configuration values are maintained within the project configuration files and shared PowerShell library.

Examples include:

* API Port
* Ollama Endpoint
* ChromaDB Endpoint
* Model Configuration
* Logging Locations

---

# Design Principles

* OpenAI API compatibility
* Stateless HTTP interface
* Persistent Windows Service
* Separation of API and infrastructure
* Retrieval-Augmented Generation support
* Local-first architecture
* Automation-friendly design

---

# Current Status

Current deployment includes:

* Windows Service hosting
* Automatic startup
* OpenAI-compatible REST API
* Ollama integration
* ChromaDB integration
* Health monitoring
* Persistent logging
* Automatic recovery after system reboot

This API serves as the primary interface for all current and future CyberByDan AI applications.
