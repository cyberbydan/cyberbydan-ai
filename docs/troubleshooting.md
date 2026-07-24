# CyberByDan AI Troubleshooting

> Common problems, diagnostics, and recovery procedures.

---

# API does not start

## Symptoms

* OpenAI API unavailable
* ai-health.ps1 reports API failure
* ai-status.ps1 reports API stopped

## Checks

```powershell
Get-Service CyberByDanAI
```

```powershell
Get-Content C:\homelab\logs\api-error.log -Tail 50
```

## Resolution

* Verify Ollama is running.
* Verify ChromaDB is running.
* Restart the platform.

```powershell
.\scripts\ai-restart.ps1
```

---

# ChromaDB unavailable

## Symptoms

* Health check fails
* API startup fails
* Retrieval unavailable

## Checks

```powershell
podman ps
```

## Resolution

```powershell
podman start chromadb
```

If the container no longer exists:

```powershell
podman-compose -f C:\docker\ai\docker-compose.yml up -d
```

---

# Ollama unavailable

## Symptoms

* No models returned
* Chat requests fail

## Checks

```powershell
ollama list
```

## Resolution

```powershell
ollama serve
```

---

# Windows Service not running

## Checks

```powershell
Get-Service CyberByDanAI
```

## Resolution

```powershell
Start-Service CyberByDanAI
```

or

```powershell
.\scripts\ai-start.ps1
```

---

# Health check fails

Run

```powershell
.\scripts\ai-health.ps1
```

Review the first failing component before investigating downstream services.

---

# Log Files

Application

```text
C:\homelab\logs\api.log
```

Errors

```text
C:\homelab\logs\api-error.log
```

---

# Escalation Order

Always troubleshoot in this order:

1. Windows Service
2. Ollama
3. ChromaDB
4. API
5. Retrieval
6. Client applications

This sequence minimizes unnecessary debugging by resolving dependency failures first.
