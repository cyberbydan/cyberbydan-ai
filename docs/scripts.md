# CyberByDan AI Scripts

> Operational PowerShell toolkit for managing the CyberByDan AI platform.

---

# Overview

The CyberByDan AI PowerShell toolkit provides a single operational interface for managing the local AI platform.

All scripts share a common library (`ai-common.ps1`) for configuration, formatting, logging, and helper functions.

---

# Script Directory

```text
scripts/

├── ai-common.ps1
├── ai-start.ps1
├── ai-stop.ps1
├── ai-restart.ps1
├── ai-status.ps1
├── ai-health.ps1
└── ai-update.ps1
```

---

# Common Library

## ai-common.ps1

Shared functionality used by every management script.

Responsibilities

* Platform configuration
* Console formatting
* Status messages
* Section headers
* Success and failure handlers
* Shared variables

This file should be imported by every AI management script.

---

# Lifecycle Scripts

## ai-start.ps1

Purpose

* Verify Ollama
* Verify API
* Start the API if required
* Wait for API readiness
* Display available models

---

## ai-stop.ps1

Purpose

* Locate the CyberByDanAI service process
* Stop the API
* Verify shutdown
* Display platform status

---

## ai-restart.ps1

Purpose

* Execute ai-stop.ps1
* Execute ai-start.ps1
* Verify successful restart

---

# Monitoring Scripts

## ai-status.ps1

Displays

* API status
* Ollama status
* ChromaDB status
* API endpoint
* Installed models
* Log locations

---

## ai-health.ps1

Verifies

* OpenAI API
* Ollama
* ChromaDB
* Chat model
* Embedding model

Returns an overall platform health assessment.

---

# Maintenance

## ai-update.ps1

Performs platform validation.

Checks

* Python environment
* Required packages
* Installed models
* ChromaDB connectivity

---

# Logging

Application log

```text
C:\homelab\logs\api.log
```

Error log

```text
C:\homelab\logs\api-error.log
```

---

# Usage

Examples

```powershell
.\scripts\ai-start.ps1
```

```powershell
.\scripts\ai-stop.ps1
```

```powershell
.\scripts\ai-restart.ps1
```

```powershell
.\scripts\ai-status.ps1
```

```powershell
.\scripts\ai-health.ps1
```

```powershell
.\scripts\ai-update.ps1
```

---

# Design Goals

The toolkit is designed to provide:

* Consistent output
* Shared codebase
* Easy maintenance
* Production-style operations
* Simple troubleshooting
* Reliable lifecycle management
