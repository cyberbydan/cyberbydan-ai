# Homelab Architecture
**Version:** 5.0
**Last Updated:** 2026-07-07
**Maintained by:** Dan Isaaka
**Status:** Active — two-machine ecosystem, EliteBook + Storm both operational

---

## Changelog

| Version | Date       | Changes                                                                                                                                                                                                                                                                                                                                      |
| ------- | ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | —          | Initial plan                                                                                                                                                                                                                                                                                                                                 |
| 2.0     | 2026-06-10 | DNS strategy decided, Windows PC added, Traefik-per-machine architecture confirmed                                                                                                                                                                                                                                                           |
| 3.0     | 2026-06-17 | Traefik replaced by Caddy, migration waves updated to reflect actual state, Superbot V2 added, backup system documented                                                                                                                                                                                                                      |
| 4.0     | 2026-06-30 | Storm connected and fully integrated. Ollama + Open WebUI deployed. Full media stack migrated from Elitebook to Storm. Jellyfin reinstalled bare metal on Storm with GPU transcoding. Tailscale DNS issue resolved. Glances monitoring added. Homepage rebuilt.                                                                              |
| 5.0     | 2026-07-07 | Docker Desktop replaced with Podman. Open WebUI moved from container to native Windows install. backup-storm.ps1 deployed — Storm now has full backup coverage. Jellyfin registered as NSSM Windows service. Port proxy setup for Podman networking. n8n secure cookie fix. n8n workflows partially restored after accidental database loss. |

---

## Infrastructure Inventory

### Primary Host — HP EliteBook 840 G3
- **OS:** Ubuntu 24 (Docker Compose)
- **Role:** Core infrastructure — DNS, reverse proxy, automation, monitoring, backups
- **Access:** Tailscale (`100.101.50.13`) + LAN (`192.168.100.28`)
- **Status:** ✅ Fully operational

### Secondary Host — Storm (Windows 11 Pro)
- **CPU:** AMD Ryzen 5 7700
- **GPU:** NVIDIA RTX 3060 12GB
- **RAM:** 16GB+
- **OS:** Windows 11 Pro
- **Role:** AI stack (Ollama, Open WebUI) + full media stack (GPU transcoding, downloads, libraries)
- **Access:** Tailscale (`100.118.211.39`) + LAN (`192.168.100.36`)
- **Status:** ✅ Fully operational
- **Container runtime:** Podman (replaced Docker Desktop 2026-07-07 for gaming compatibility)
- **Constraint:** Also used for gaming. Driver signature enforcement bypass breaks Hyper-V/WSL2/Docker Desktop — Podman was chosen as the container runtime specifically to avoid this conflict.

---

## Current Services

### Infrastructure (Elitebook)
| Service     | URL              | Status                           |
| ----------- | ---------------- | -------------------------------- |
| Homepage    | home.danlab      | ✅ Running                        |
| Portainer   | portainer.danlab | ✅ Running                        |
| Code Server | code.danlab      | ✅ Running                        |
| Pi-hole     | pihole.danlab    | ✅ Running — listening mode ALL   |
| Caddy       | Reverse proxy    | ✅ Running — routing all services |
| Authentik   | authentik.danlab | ✅ Running — SSO not yet enforced |

### Automation (Elitebook)
| Service   | URL                 | Status                                                            |
| --------- | ------------------- | ----------------------------------------------------------------- |
| n8n       | n8n.danlab          | ✅ Running — N8N_SECURE_COOKIE=false, workflows partially restored |
| Superbot  | Telegram            | ✅ Running as systemd service                                      |
| Flask API | 192.168.100.28:5050 | ✅ Running as systemd service                                      |

### Observability (Elitebook)
| Service     | URL            | Status                                           |
| ----------- | -------------- | ------------------------------------------------ |
| Grafana     | grafana.danlab | ✅ Running                                        |
| Loki        | Internal       | ✅ Running                                        |
| Promtail    | Internal       | ✅ Running                                        |
| Uptime Kuma | kuma.danlab    | ✅ Running — Telegram notifications still pending |

### AI Stack (Storm)
| Service    | URL                    | Status                                                       |
| ---------- | ---------------------- | ------------------------------------------------------------ |
| Ollama     | ollama.danlab:11434    | ✅ Running — native Windows, GPU accelerated (RTX 3060)       |
| Open WebUI | open-webui.danlab:3000 | ✅ Running — native Windows (NSSM service), not containerised |

### Media Stack (Storm — Podman)
| Service      | URL               | Status                                                         |
| ------------ | ----------------- | -------------------------------------------------------------- |
| Jellyfin     | jellyfin.danlab   | ✅ Running — bare metal Windows service (NSSM), GPU transcoding |
| Jellyseerr   | jellyseerr.danlab | ✅ Running — Podman                                             |
| Sonarr       | sonarr.danlab     | ✅ Running — Podman                                             |
| Radarr       | radarr.danlab     | ✅ Running — Podman                                             |
| Lidarr       | lidarr.danlab     | ✅ Running — Podman                                             |
| Prowlarr     | prowlarr.danlab   | ✅ Running — Podman                                             |
| Bazarr       | bazarr.danlab     | ✅ Running — Podman                                             |
| qBittorrent  | qbit.danlab       | ✅ Running — Podman                                             |
| Navidrome    | navidrome.danlab  | ✅ Running — Podman                                             |
| FlareSolverr | Internal          | ✅ Running — Podman                                             |

### Monitoring — Storm
| Service | Access               | Status                              |
| ------- | -------------------- | ----------------------------------- |
| Glances | 100.118.211.39:61208 | ✅ Running as Windows service (NSSM) |

---

## Container Runtime — Storm

### Choice: Podman (replaces Docker Desktop)

Docker Desktop was the original choice but was replaced in Session 07 for gaming compatibility.

**Why Podman:**
- Does not require Hyper-V — uses WSL2 in rootful mode without the Windows Hypervisor Platform feature
- Games that require driver signature enforcement bypass can coexist without breaking containers
- Drop-in Docker replacement — same compose file format, same image registries
- Red Hat-backed, long-term supported

**Podman on Windows networking — known limitations:**
Podman on Windows does not bind container ports to the host's LAN or Tailscale interfaces by default — only to localhost (`127.0.0.1`). This required a `netsh portproxy` workaround to expose services to the network.

**Port proxy setup:**
Two sets of rules are maintained via `C:\homelab\scripts\setup-port-proxy.ps1`:
- LAN IP (`192.168.100.36`) → `127.0.0.1` for each service port
- Tailscale IP (`100.118.211.39`) → `127.0.0.1` for each service port

This script runs at startup via a dedicated Task Scheduler entry (`PodmanPortProxy`). Without it, services are only reachable from Storm's localhost — not from other devices on the network or Tailscale.

**Ollama + Open WebUI networking issue:**
Podman's internal VM cannot reach the Windows host's network stack cleanly. `host.docker.internal` does not resolve correctly in Podman on Windows (resolves to `10.88.0.1` but that gateway is inaccessible). As a result, Open WebUI cannot run inside Podman and talk to native Ollama. **Resolution:** Open WebUI was moved to a native Windows install (pip + NSSM service), where it connects to Ollama at `localhost:11434` with no container boundary.

**Auto-start:**
- Podman machine starts via NSSM or is already running on login
- `C:\homelab\scripts\start-podman-stacks.ps1` runs at logon via Task Scheduler (`PodmanAutoStart`) — starts the Podman machine, waits 30s, brings up the media stack, then runs the port proxy script
- Jellyfin, Open WebUI, Glances, and Ollama run as native Windows services (NSSM) — auto-start independently of Podman

---

## Backup System

### Elitebook — three decks (partially active)

- **Infrastructure Deck** — `backup-infra.sh`, daily 2:00am ✅
- **Media Deck** — `backup-media.sh`, weekly Sunday 3:00am ⚠️ **now backs up nothing** — media moved to Storm. Needs retiring or repointing to Storm's DBs.
- **Control Panel Deck** — `backup-control-panel.sh`, daily 2:30am ✅

### Storm — backup-storm.ps1 (new, deployed 2026-07-07)

**Script:** `C:\homelab\scripts\backup-storm.ps1`
**Schedule:** Daily 2:00am via Windows Task Scheduler (`BackupStorm`)
**Runtime:** ~30 minutes (first run; subsequent runs faster due to Restic deduplication)
**Status:** ✅ First run completed successfully — all 10 steps green

**What it backs up:**
- Sonarr, Radarr, Lidarr, Prowlarr DB files
- Bazarr DB (`db/bazarr.db` — note: not the root-level bazarr.db)
- Jellyseerr DB (WAL checkpoint — stops container, copies `db/db.sqlite3`, restarts)
- Jellyfin config + library DB (`C:\ProgramData\Jellyfin\Server`)
- Open WebUI data volume (exported via Alpine helper container, cache excluded)
- Restic snapshot → `C:\restic-repo`
- rclone sync → Google Drive (`homelab-storm-backup:homelab-storm-backup`)

**JSON log:** `C:\homelab\backups\last-storm-backup.json`

**Restic repo:** `C:\restic-repo`
**RESTIC_PASSWORD:** stored as Windows System environment variable — never hardcoded
**rclone remote:** `homelab-storm-backup` (Google Drive, same account as Elitebook)

---

## n8n — current state after Session 07

**Problem:** n8n container was recreated as part of the `N8N_SECURE_COOKIE=false` fix, and the bind mount was not receiving writes — database was stored inside the container, not on the host. Container recreate wiped the database.

**Recovery:** workflows-export.json was current (auto-export had run at 6am same day). 2 of 6 workflows imported successfully via CLI. 4 workflows (backup reports, git export) failed due to SQLITE_CONSTRAINT foreign key errors — believed to be a version compatibility issue between the export format and n8n v2.22.6.

**Current state:**
- Workflows in n8n: TEST-PERSISTENCE ✅, Mobile Payments ✅
- Workflows needing manual recreation: Control Panel Backup Report, Media Stack Backup, Infra Backup Report, n8n Workflow Export to Git
- Bind mount verified working after recreation — persistence-test confirmed
- `N8N_SECURE_COOKIE=false` added to compose environment

**Technical debt:** recreate the 4 missing workflows manually in the n8n UI and reconnect the Telegram credential.

---

## Storm — Windows Services (NSSM)

All long-running services on Storm that are not Podman containers run as Windows services via NSSM:

| Service    | NSSM name          | Executable            | Port  |
| ---------- | ------------------ | --------------------- | ----- |
| Ollama     | (native installer) | ollama.exe            | 11434 |
| Open WebUI | OpenWebUI          | open-webui.exe        | 3000  |
| Jellyfin   | JellyfinServer     | jellyfin.exe          | 8096  |
| Glances    | GlancesWeb         | python.exe -m glances | 61208 |

**Jellyfin data directory:** `C:\ProgramData\Jellyfin\Server` — must be passed explicitly via `--datadir` argument. Do NOT launch `jellyfin.exe` without this flag or it will create a fresh empty config at `%LOCALAPPDATA%\jellyfin` and present the setup wizard.

**Open WebUI:** installed via pip into Python 3.11. OLLAMA_BASE_URL set to `http://localhost:11434` via NSSM AppEnvironmentExtra.

---

## Storm — Port Proxy

Podman only binds to `127.0.0.1` on Windows. To expose services to LAN and Tailscale:

```powershell
# Script: C:\homelab\scripts\setup-port-proxy.ps1
$ports = @(8989, 7878, 9696, 6767, 8080, 5055, 8686, 4533, 8191, 3000)
$lanIP = "192.168.100.36"
$tailscaleIP = "100.118.211.39"

foreach ($port in $ports) {
    netsh interface portproxy add v4tov4 listenaddress=$lanIP listenport=$port connectaddress=127.0.0.1 connectport=$port
    netsh interface portproxy add v4tov4 listenaddress=$tailscaleIP listenport=$port connectaddress=127.0.0.1 connectport=$port
}
```

Runs at startup via Task Scheduler (`PodmanPortProxy`, SYSTEM account).

**Verify rules are active:**
```powershell
netsh interface portproxy show all
```

**If rules are missing after reboot:** run `setup-port-proxy.ps1` manually as administrator, then check Task Scheduler for why the task didn't fire.

---

## Storm — hosts file overrides

Storm's `C:\Windows\System32\drivers\etc\hosts` maps `.danlab` domains to `192.168.100.36` (Storm's LAN IP) so that Storm can reach its own services directly without hairpin routing through Caddy on the Elitebook:

```
192.168.100.36 sonarr.danlab
192.168.100.36 radarr.danlab
192.168.100.36 prowlarr.danlab
192.168.100.36 bazarr.danlab
192.168.100.36 qbit.danlab
192.168.100.36 jellyseerr.danlab
192.168.100.36 lidarr.danlab
192.168.100.36 navidrome.danlab
192.168.100.36 jellyfin.danlab
192.168.100.36 open-webui.danlab
192.168.100.36 ollama.danlab
```

These entries must be maintained manually if services move or IPs change.

---

## Folder Structure

### Elitebook
```
homelab/
├── scripts/
│   ├── backup-api.py
│   ├── backup-infra.sh
│   ├── backup-media.sh         # ⚠️ backs up nothing — media moved to Storm
│   └── backup-control-panel.sh
├── infrastructure/
│   ├── docker-compose.yml      # n8n, Portainer, Grafana, code-server — N8N_SECURE_COOKIE=false added
│   └── caddy/
│       └── Caddyfile           # ⚠️ stale copy — real file is /opt/docker/caddy/config/Caddyfile
├── services/infra/homepage/config/   # ✅ REAL Homepage config path
├── control-plane/homepage/config/    # ⚠️ stale/unused — Homepage does not read this
├── storm/                      # Storm configs, version-controlled
│   ├── media-docker-compose.yml
│   ├── start-podman-stacks.ps1
│   ├── setup-port-proxy.ps1
│   └── backup-storm.ps1
└── docs/
    ├── sessions/
    │   ├── session-05.md
    │   ├── session-06.md
    │   └── session-07.md
    ├── lessons-learned.md
    ├── recovery-playbooks.md
    └── state-inventory.md
```

### Storm
```
C:\
├── docker\media\               # Podman compose + config folders
│   └── docker-compose.yml      # long-form bind mount syntax (E:/ paths)
├── homelab\                    # Git clone — shared repo with Elitebook
│   ├── scripts\
│   │   ├── backup-storm.ps1
│   │   ├── start-podman-stacks.ps1
│   │   └── setup-port-proxy.ps1
│   └── backups\
│       └── last-storm-backup.json
├── restic-repo\                # Local Restic repository
└── ProgramData\Jellyfin\Server\ # Jellyfin data — real path, NOT %AppData%

E:\media\
├── movies\
├── series\
├── music\
└── downloads\
```

---

## Pending Items — Next Sessions

| Item                                      | Priority      | Notes                                                                                                                            |
| ----------------------------------------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Recreate 4 missing n8n workflows          | **High**      | Control Panel Backup Report, Media Stack Backup, Infra Backup Report, n8n Workflow Export to Git — manual UI recreation required |
| Retire or repoint backup-media.sh         | High          | Currently backs up an empty Elitebook media stack — wastes a backup slot                                                         |
| Uptime Kuma Telegram notifications        | High          | Carried over from Session 5 — 4 sessions without action                                                                          |
| Authentik SSO enforcement                 | High          | Carried over from Session 5                                                                                                      |
| Superbot V3                               | Medium        | API keys to .env, backup triggers                                                                                                |
| Superbot V4 — AI agent                    | Now unblocked | Ollama live on Storm, Flask API on Elitebook — architecture ready                                                                |
| Verify Storm backup on next scheduled run | Medium        | First run was manual — confirm the 2am Task Scheduler fires correctly                                                            |
| Gaming coexistence testing                | Medium        | Podman is now in place — test that games work without breaking services                                                          |

---

## Engineering Principles

1. Preserve uptime — incremental changes only
2. Avoid unnecessary complexity
3. Tailscale is the primary security boundary
4. Maintain and verify backups before any major change
5. Every migration step has a rollback path
6. Version control all config files — if it's not in Git it doesn't exist
7. Verify bind mounts are receiving writes before relying on them for state
8. UFW on a Docker host requires explicit rules per port — the LAN subnet rule does not cover Docker bridge traffic
9. Design for future AI services from the start
10. Verify the real mounted config path with `docker inspect` before editing — never trust documentation alone
11. When extending infrastructure across multiple physical hosts, plan DNS and firewall rules for cross-host traffic explicitly
12. **New — Podman on Windows does not expose container ports to the host network by default.** Always run `setup-port-proxy.ps1` after any Podman networking change and verify with `netsh interface portproxy show all`
13. **New — never launch Jellyfin.exe without the `--datadir` flag on Storm.** Without it, a fresh empty config is created at `%LOCALAPPDATA%\jellyfin` and the real data at `C:\ProgramData\Jellyfin\Server` is ignored