# CyberByDan AI Services

> Operational services that make up the CyberByDan AI platform.

---

# Overview

CyberByDan AI consists of three persistent runtime services:

* CyberByDanAI (Windows Service)
* Ollama
* ChromaDB

These services work together to provide a production-ready local AI platform.

---

# Service Architecture

```text
Clients

↓

CyberByDanAI Service

↓

Ollama

↓

ChromaDB
```

---

# CyberByDanAI

Type

```
Windows Service
```

Service Name

```
CyberByDanAI
```

Manager

```
NSSM
```

Startup

```
Automatic
```

Purpose

* Hosts the FastAPI application
* Exposes the OpenAI-compatible API
* Handles retrieval and prompt construction
* Routes requests to Ollama

Health Check

```powershell
Get-Service CyberByDanAI
```

---

# Ollama

Type

```
Windows Application
```

Purpose

* Hosts local language models
* Performs inference
* Generates embeddings

Endpoint

```
http://127.0.0.1:11434
```

Health Check

```powershell
ollama list
```

---

# ChromaDB

Type

```
Podman Container
```

Container

```
chromadb
```

Compose Stack

```
C:\docker\ai
```

Purpose

* Stores vector embeddings
* Performs similarity search
* Provides retrieval context

Health Check

```powershell
podman ps
```

---

# Service Dependencies

Startup order

```text
Windows

↓

Podman Machine

↓

ChromaDB

↓

Ollama

↓

CyberByDanAI
```

The API depends on both Ollama and ChromaDB being available.

---

# Management

The AI platform is managed using the PowerShell toolkit.

Available commands

* ai-start.ps1
* ai-stop.ps1
* ai-restart.ps1
* ai-status.ps1
* ai-health.ps1
* ai-update.ps1

---

# Logging

Application

```
C:\homelab\logs\api.log
```

Errors

```
C:\homelab\logs\api-error.log
```

---

# Operational Status

Current platform services

| Service      | Status     |
| ------------ | ---------- |
| CyberByDanAI | Production |
| Ollama       | Production |
| ChromaDB     | Production |

All services have been verified to recover successfully after a full Windows reboot.
