# Superbot Architecture

**Version:** 1.0
**Last updated:** 2026-06-08
**Status:** V1 in progress

---

## What is Superbot?

> Superbot is a personal homelab control plane that gives me observability and safe operational control over my entire infrastructure without needing to SSH into the host, open a browser, or remember service URLs.

Telegram is the current interface. The control plane is the product.

---

## Design Principles

1. **The Flask API is the only thing that touches infrastructure.** Every interface is just a renderer.
2. **Read-heavy by default.** Observability first, actions second.
3. **No destructive actions in V1 or V2.** If it can't be undone, it doesn't belong in the bot.
4. **Every action is logged.** Timestamp, user, action, outcome.
5. **Interface-agnostic.** Today Telegram. Tomorrow anything.

---

## Architecture

Three layers, strict boundaries:

```
┌─────────────────────────────────┐
│         Interface Layer          │
│   Telegram · Web · CLI · AI      │
└────────────────┬────────────────┘
                 │ HTTP only
┌────────────────▼────────────────┐
│        Control Plane             │
│       Flask API (port 5050)      │
│  System · Backup · Container     │
│  Media · Monitoring · Automation │
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│       Infrastructure Layer       │
│  Docker · Jellyfin · Scripts     │
│  Grafana · n8n · Uptime Kuma     │
└─────────────────────────────────┘
```

**The rule:** Superbot (Telegram) only speaks to the Flask API via HTTP. It never runs shell commands directly. It never touches Docker directly. It never reads files directly.

---

## Current Capabilities (V1)

### System
- Disk usage
- RAM usage
- Uptime
- Full health check (containers running, CPU, memory, Tailscale status, last backup times)

### Backups
- View status for infra, media, control panel decks
- Trigger infra, media, control panel backups on demand

### Containers
- List running containers

### Interface
- Inline keyboard menu navigation
- Private access (allowlist by Telegram username)

---

## Flask API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Full system health check |
| GET | `/backup/infra/status` | Last infra backup result |
| GET | `/backup/media/status` | Last media backup result |
| GET | `/backup/control-panel/status` | Last control panel backup result |
| POST | `/backup/infra` | Trigger infra backup |
| POST | `/backup/media` | Trigger media backup |
| POST | `/backup/control-panel` | Trigger control panel backup |

---

## Modules

### System Module
**Purpose:** Host observability
**Current:** Disk, RAM, uptime via health endpoint
**Future:** Historical trends, threshold alerts, per-service resource usage

### Backup Module
**Purpose:** Backup visibility and control
**Current:** Status and trigger for all three decks
**Future:** Backup history, restore verification, last successful restore date

### Container Module
**Purpose:** Docker visibility
**Current:** List running containers
**Future:** Per-container stats, restart capability (safe, reversible action)

### Media Module *(not yet built)*
**Purpose:** Media stack visibility
**Current:** None
**Future:** Sonarr/Radarr queue, active downloads, disk usage by media type, recent requests

### Monitoring Module *(not yet built)*
**Purpose:** Proactive alerting
**Current:** None
**Future:** Uptime Kuma webhook → Superbot notification, Grafana alert routing

### Automation Module *(not yet built)*
**Purpose:** n8n workflow control
**Current:** None
**Future:** Trigger workflows on demand, view execution history

---

## Roadmap

### V1 — Solid Foundation *(current)*
- [x] Menu-driven Telegram interface
- [x] System metrics
- [x] Backup trigger and status
- [x] Container listing
- [ ] All actions routed through Flask API (shell commands still in bot — migrate these)
- [ ] Structured action logging

### V2 — Operational Maturity
- [ ] Media module — download queue, requests, disk usage
- [ ] Monitoring module — proactive Uptime Kuma alerts
- [ ] Container module fully through Flask API using Docker SDK
- [ ] n8n workflow triggers
- [ ] Action log — every command recorded with timestamp and outcome

### V3 — Intelligence Layer
- [ ] Daily digest — scheduled system health summary to Telegram
- [ ] Anomaly detection — disk growth, memory spikes, unusual container restarts
- [ ] Smart alerts — context-aware, not just raw triggers
- [ ] Natural language interface

### V4 — Personal Operating System
- [ ] Web dashboard
- [ ] Multi-node support (Windows desktop)
- [ ] Self-healing workflows — detect down service, attempt restart, notify
- [ ] Audit reports generated from operational data

---

## Known Technical Debt

| Item | Risk | Priority |
|------|------|----------|
| Shell commands (`run()`) still in superbot.py | Bypasses API layer, creates maintenance burden | High |
| No action logging | Cannot audit what was triggered and when | Medium |
| Flask API has no auth | Any process on localhost can trigger backups | Low (single host) |
| Superbot has no systemd service yet | Not auto-starting on reboot | Medium |

---

## File Locations

| File | Purpose |
|------|---------|
| `~/homelab/telegram-bots/superbot.py` | Telegram interface |
| `~/homelab/scripts/backup-api.py` | Flask control plane |
| `~/homelab/scripts/health_check.sh` | System health script called by Flask |
| `~/homelab/telegram-bots/.env` | Bot tokens and allowed users (not in Git) |