# CyberByDan AI Deployment

> Deployment guide for a fresh CyberByDan AI installation.

---

# Overview

This document describes how to deploy the CyberByDan AI platform on a new Windows machine.

The completed deployment consists of:

* Ollama
* ChromaDB
* CyberByDanAI Windows Service
* PowerShell management toolkit

---

# Prerequisites

Required software

* Git
* Python 3.11+
* Ollama
* Podman Desktop
* NSSM
* PowerShell 7 (recommended)

---

# Repository

Clone the repository.

```powershell
git clone <repository-url>
```

---

# Python Environment

Create the virtual environment.

```powershell
python -m venv .venv
```

Activate it.

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies.

```powershell
pip install -r requirements.txt
```

---

# Ollama

Install the required models.

```powershell
ollama pull deepseek-r1:14b
ollama pull nomic-embed-text
```

Verify installation.

```powershell
ollama list
```

---

# ChromaDB

Deploy the AI stack.

```powershell
podman-compose -f C:\docker\ai\docker-compose.yml up -d
```

Verify.

```powershell
podman ps
```

---

# Windows Service

Install the API service using NSSM.

Service

```text
CyberByDanAI
```

Startup

```text
Automatic
```

Logs

```text
C:\homelab\logs
```

---

# Validation

Run the health check.

```powershell
.\scripts\ai-health.ps1
```

Expected result

```text
CyberByDan AI is HEALTHY
```

---

# Management

Daily management is performed using:

* ai-start.ps1
* ai-stop.ps1
* ai-restart.ps1
* ai-status.ps1
* ai-health.ps1
* ai-update.ps1

---

# Deployment Complete

A successful deployment provides:

* OpenAI-compatible API
* Persistent Windows Service
* Ollama integration
* ChromaDB retrieval
* Automatic recovery after reboot
* Production-ready local AI platform
