# CyberByDan AI Operations

> Operational runbook for the CyberByDan AI platform.

---

# Daily Operations

## Check platform status

```powershell
.\scripts\ai-status.ps1
```

---

## Verify platform health

```powershell
.\scripts\ai-health.ps1
```

---

## Restart the platform

```powershell
.\scripts\ai-restart.ps1
```

---

## Stop the API

```powershell
.\scripts\ai-stop.ps1
```

---

## Start the API

```powershell
.\scripts\ai-start.ps1
```

---

# Routine Maintenance

## Validate platform

```powershell
.\scripts\ai-update.ps1
```

Recommended after:

* Pulling repository updates
* Updating Python packages
* Updating Ollama
* Updating ChromaDB
* Updating models

---

# Troubleshooting

## API unavailable

Check

```powershell
Get-Service CyberByDanAI
```

If stopped

```powershell
.\scripts\ai-start.ps1
```

---

## ChromaDB unavailable

Check

```powershell
podman ps
```

If stopped

```powershell
podman start chromadb
```

---

## Ollama unavailable

Check

```powershell
ollama list
```

If necessary

```powershell
ollama serve
```

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

# Recovery Sequence

If the platform is unhealthy:

1. Run `ai-health.ps1`
2. Review `api-error.log`
3. Confirm CyberByDanAI service is running.
4. Confirm Ollama is running.
5. Confirm ChromaDB container is running.
6. Execute `ai-restart.ps1` if required.

---

# Expected Healthy State

A healthy platform satisfies all of the following:

* CyberByDanAI Windows Service is running.
* Ollama is responding.
* ChromaDB container is running.
* OpenAI API is reachable.
* Chat model is available.
* Embedding model is available.
* `ai-health.ps1` reports **HEALTHY**.
