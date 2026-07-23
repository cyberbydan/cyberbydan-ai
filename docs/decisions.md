# AI Architectural Decisions

This document records important architectural decisions made during the development of the CyberByDan AI Platform. Each decision includes the reasoning behind it and serves as a historical record for future maintenance and refactoring.

---

# 2026-07-23 — AI Platform Infrastructure Stabilization

## Decision

The CyberByDan AI platform will operate as a collection of independent infrastructure services rather than a single manually launched application.

## Motivation

Originally, the AI API was started manually from VS Code using Uvicorn. This required an active terminal session and prevented the platform from operating unattended or surviving system reboots.

The objective was to transform the AI into a persistent operating service capable of serving requests from any OpenAI-compatible client at any time.

---

# Windows Service

## Decision

The FastAPI application is hosted as a native Windows Service using NSSM.

### Previous

VS Code

↓

PowerShell

↓

python -m uvicorn

### Current

Windows

↓

CyberByDanAI Windows Service

↓

FastAPI

---

## Benefits

* Starts automatically after boot.
* No visible PowerShell windows.
* Independent of user logins.
* Managed through Windows Service Control Manager.
* Centralized logging.
* Automatic restart on failure.

---

# API Lifecycle Management

## Decision

A dedicated PowerShell management toolkit was created.

### Scripts

* ai-start.ps1
* ai-stop.ps1
* ai-restart.ps1
* ai-status.ps1
* ai-health.ps1
* ai-update.ps1
* ai-common.ps1

---

## Motivation

Development should never require manually typing long Uvicorn commands.

The toolkit provides a consistent operational interface for developers and future automation.

---

# Logging

## Decision

API logs are redirected through NSSM.

### Files

logs/api.log

logs/api-error.log

---

## Benefits

* Persistent logs
* Easier debugging
* No console dependency

---

# ChromaDB Deployment

## Decision

ChromaDB is managed through Podman Compose.

### Previous

Standalone manually-created container.

### Current

Dedicated AI compose stack.

```
C:\docker\ai\
    docker-compose.yml
```

---

## Motivation

The vector database is now considered permanent AI infrastructure.

Compose provides:

* reproducibility
* automatic startup
* version-controlled configuration
* easier migration

---

# Infrastructure Separation

## Decision

Media services and AI services remain independent Compose projects.

### Media

```
C:\docker\media\
```

Contains:

* Sonarr
* Radarr
* Lidarr
* Bazarr
* Prowlarr
* Jellyseerr
* qBittorrent
* FlareSolverr
* Navidrome

### AI

```
C:\docker\ai\
```

Currently contains:

* ChromaDB

Future additions may include:

* Open WebUI
* MCP Servers
* Redis
* PostgreSQL
* Vector services
* AI utilities

---

## Motivation

Media infrastructure and AI infrastructure evolve independently.

Keeping them separate reduces coupling and simplifies maintenance.

---

# Startup Architecture

## Decision

System startup is layered.

```
Windows

↓

Podman Machine

↓

Media Compose Stack

↓

AI Compose Stack

↓

Ollama

↓

CyberByDanAI Windows Service
```

---

## Motivation

Each layer is responsible only for its own resources.

The API consumes infrastructure but does not manage it.

---

# Chroma Initialization

## Decision

The retriever now performs lazy initialization.

Instead of connecting to Chroma during Python module import, the connection is created only when retrieval is first required.

---

## Motivation

Prevents application startup failures when Chroma is still initializing.

Improves service resilience.

---

# OpenAI Compatibility

## Decision

CyberByDan AI exposes an OpenAI-compatible REST API.

This allows any OpenAI-compatible application to communicate with the local AI without modification.

Examples include:

* Open WebUI
* n8n
* Telegram bots
* WhatsApp bots
* Custom applications
* Future desktop clients

---

# Health Monitoring

## Decision

Platform health is verified through ai-health.ps1.

Checks include:

* OpenAI API
* Ollama
* ChromaDB
* Embedding model
* Chat model

---

## Motivation

Health should be determined through actual service availability rather than process existence.

---

# Operational Milestone

## Achievement

The CyberByDan AI Platform now:

* survives Windows reboot
* automatically restores infrastructure
* automatically restores AI services
* automatically restores the OpenAI API
* requires no manual terminal interaction
* exposes a persistent OpenAI-compatible endpoint
* maintains a healthy operational state after boot

This marks the completion of the initial AI infrastructure phase.
