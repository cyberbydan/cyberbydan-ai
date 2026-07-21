# CyberByDan Homelab

> "A healthy obsession built on a modest EliteBook."

This started about a month ago with a simple idea — stream movies across devices on the home network. One Jellyfin container later, something clicked. Then came the next service, and the next, and the next. Building, breaking, troubleshooting, learning. Repeat.

What started as a media server is now a full self-hosted infrastructure stack running on an HP EliteBook 840 G3 with 8GB of RAM and 250GB of SSD. Nothing fancy. Just curiosity and persistence.

This repository is the living record of that journey.

---

## The Journey

### Month 1 — It started with movies
Jellyfin was the spark. Getting it running, accessible across the network, and stable was the first real win. From there the question became: *what else can I run?*

### The stack started growing
One service led to another. A download stack to feed Jellyfin. A reverse proxy to manage access. A monitoring stack to see what was actually happening. An identity provider so every service had proper authentication. An automation engine to tie it all together.

Each new service taught something new — networking, volumes, compose files, DNS, permissions.

### The first major incident
All n8n workflows and credentials were lost overnight. A Docker bind mount had been misconfigured from the start — the container was writing state to its own internal filesystem, not the host volume. When the container was recreated, everything was gone.

No warning. No error. Just gone.

That incident changed how the entire lab is operated. Backup architecture was rebuilt from scratch. A state inventory was created. Recovery playbooks were written. Everything went into Git.

### Where it is now
The lab is stable, documented, and version controlled. Every service has a backup path. Every incident has a post-mortem. The homelab now runs:

- A full media stack with automated downloads, subtitles, and requests
- SSO across all services via an open source identity provider
- A centralised dashboard with live service status
- Metrics, logs, and uptime monitoring across the entire stack
- Scheduled backups with offsite replication to Google Drive
- Workflow automation bridged to backup scripts via a custom API
- Three Telegram bots for remote monitoring and control
- HTTPS on all services via a local CA and wildcard DNS on *.danlab
- Automated subtitle downloads across the entire media library

And it all runs on one EliteBook.

---

## Hardware

| Device | Specs | Role |
|--------|-------|------|
| HP EliteBook 840 G3 | 8GB RAM, 250GB SSD, Ubuntu | Primary host — runs everything |
| Windows Desktop (pending) | Ryzen 7700, RTX 3060 | Future node |
| External SSD | 120GB | Additional storage |

---

## Stack

### Infrastructure
| Service | Purpose |
|---------|---------|
| Portainer | Container management UI |
| Authentik | SSO / Identity provider |
| Pi-hole | DNS filtering, ad blocking, and local *.danlab resolution |
| Caddy | Reverse proxy — HTTPS for *.danlab via local CA |
| Tailscale | Secure remote access |
| code-server | Browser-based IDE |

### Monitoring & Observability
| Service | Purpose |
|---------|---------|
| Grafana | Metrics dashboards |
| Loki | Log aggregation |
| Promtail | Log shipping |
| Uptime Kuma | Service uptime monitoring |

### Control Plane
| Service | Purpose |
|---------|---------|
| Homepage | Centralised service dashboard |

### Media
| Service | Purpose |
|---------|---------|
| Jellyfin | Media server — where it all began |
| Jellyseerr | Media request management |
| Sonarr | TV show management — 1080p WEB, max 1.5GB per episode |
| Radarr | Movie management — 1080p WEB, max 4GB per movie |
| Prowlarr | Indexer management |
| Bazarr | Subtitle management — English, 5 providers |
| qBittorrent | Download client |

### Automation
| Service | Purpose |
|---------|---------|
| n8n | Workflow automation |
| Flask Backup API | Custom API bridging n8n to backup scripts |
| Telegram Bots | Remote homelab control and monitoring |

---

## Backup Architecture

Three modular scripts, each covering a logical stack:

| Script | Schedule | Covers |
|--------|----------|--------|
| `backup-infra.sh` | Daily 2:00am | Infrastructure, Authentik DB, n8n, bots, Pi-hole, Caddy |
| `backup-control-panel.sh` | Daily 2:30am | Homepage config files |
| `backup-media.sh` | Weekly Sunday 3:00am | Media stack DBs, Jellyseerr |

All snapshots go to local Restic repository and offsite to Google Drive.

---

## Directory Structure

```
homelab/
├── archive/          # Retired configs and old stack versions
├── control-plane/    # Homepage dashboard stack
├── docs/             # Incident logs, playbooks, state inventory
├── infrastructure/   # Core services (n8n, authentik, portainer, caddy config, etc.)
├── logs/             # Backup and script logs
├── loki-stack/       # Grafana, Loki, Promtail
├── media/            # Full media stack
├── scripts/          # Backup and maintenance scripts
└── telegram-bots/    # Python Telegram bots

/opt/docker/          # Migrated services (new home for infrastructure)
├── caddy/            # Reverse proxy — Caddyfile, certs, local CA
└── pihole/           # DNS — config, dnsmasq, adlists
```

---

## Documentation

| Document | Purpose |
|----------|---------|
| `docs/lessons-learned.md` | Incident log with root cause analysis |
| `docs/recovery-playbooks.md` | Step-by-step restore procedures with RTO estimates |
| `docs/state-inventory.md` | Full service catalogue with volume paths and backup coverage |

---

## Incidents

| ID | Date | Service | Summary |
|----|------|---------|---------|
| 001 | June 2026 | n8n | Workflow loss due to unverified Docker bind mount |
| 002 | 2026-06-07 | Jellyseerr | Data recovery after Jellyfin Docker→baremetal migration |
| 003 | 2026-06-11 | Pi-hole | DNS outage during network_mode:host → bridge migration |
| 004 | 2026-06-16 | Caddy | Caddyfile never persisted to disk — routing config one recreate away from total loss |
| 005 | 2026-06-16 | Traefik | Silent port conflict — Traefik holding ports 80/443 alongside Caddy, removed and archived |

---

## Key Lessons

- A service that isn't monitored is a service you're flying blind on
- A backup that isn't verified is a backup you don't have
- State that isn't inventoried is state you don't know you're losing
- For critical network services, stage the replacement before stopping the running service
- A service that appears healthy is not the same as a service that is recoverable
- Container paths and host paths are never the same thing — always verify save paths from inside the container
- A bind mount pointing to an empty file is silent misconfiguration — verify content, not just existence
- Path mappings in reverse proxies and subtitle managers are required even when containers can reach each other
- Breaking things intentionally teaches more than reading about them ever will
- Dead services holding critical ports are invisible until a restart forces the conflict — audit running containers after every major change

---

*Built on an HP EliteBook 840 G3. One month in. Just getting started.*