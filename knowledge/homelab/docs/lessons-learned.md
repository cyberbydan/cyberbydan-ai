# Lessons Learned

## Incident 001 — n8n workflow and credential loss

**Date:** June 2026
**Severity:** Medium
**Status:** Resolved — rebuild complete

### What happened

All n8n workflows and stored credentials were lost. Investigation revealed the Docker bind mount for n8n had been misconfigured — the container was writing state to its internal union filesystem rather than to the host volume. When the container was recreated, all state was gone.

### What was lost

- Infrastructure backup reporting workflow
- Media backup reporting workflow
- Early Superbot experiments
- Telegram bot credentials stored in n8n

### What survived

- All Docker Compose files
- Backup scripts (`backup-infra.sh`, `backup-media.sh`)
- Flask backup API (`backup-api.py`)
- All infrastructure and media services
- Documentation

### Root cause

**Primary:** Unverified bind mount. The volume path was defined in the Compose file but never confirmed to be receiving writes on the host filesystem.

**Secondary:** No backup coverage for n8n state. The backup scripts protected scripts and configs but not the n8n data directory.

**Contributing:** No state inventory existed. There was no document listing which services held critical state and whether that state was protected.

### Why it was not caught earlier

The container appeared healthy. There was no monitoring or alerting on whether the bind mount was active. The gap was invisible until the container was recreated.

### What changed as a result

1. Git initialized at `~/homelab` — all configuration now version-controlled
2. State inventory created at `docs/state-inventory.md`
3. n8n bind mount verified before any workflows were created
4. n8n volume added to `backup-infra.sh` coverage
5. n8n workflow JSON exports added to backup routine
6. Flask backup API added to Uptime Kuma monitoring
7. Recovery playbooks written at `docs/recovery-playbooks.md`
8. n8n Auto Export workflow built in Session 5 — exports all workflows to Git every 6 hours automatically

### CISA domain mapping

| Domain | Relevance |
|--------|-----------|
| Domain 2 — IT Governance | Absence of change management and configuration standards allowed the misconfiguration to persist |
| Domain 4 — IS Operations and Business Resilience | Backup coverage gap and lack of recovery testing directly caused data loss |
| Domain 5 — Protection of Information Assets | Credentials stored in n8n without independent backup constituted a single point of failure |

### Key principle reinforced

> Backups that are not verified are backups you do not have.
> State that is not inventoried is state you do not know you are losing.

---

## Incident 002 — Jellyseerr data recovery after Jellyfin migration

**Date:** 2026-06-07
**Severity:** Medium
**Status:** Resolved

### What happened

Jellyfin was migrated from Docker to baremetal. Jellyseerr lost its Jellyfin connection and presented the first-run setup wizard, appearing to be a full data loss event. Investigation confirmed data was intact but the SQLite WAL file had not been checkpointed into the main database file.

### What was lost

- Jellyfin connection configuration (settings.json was blank)
- 0 media requests (none existed)
- 2 user accounts (re-imported from Jellyfin)

### What survived

- All Jellyseerr state in the WAL file (2.6MB)
- Docker volume mount was correctly configured throughout
- Jellyseerr internal DB tables fully intact after WAL checkpoint

### Root cause

**Primary:** Dead Docker hostname. Jellyseerr was configured to reach Jellyfin at `jellyfin:8096` — a Docker DNS name that stopped resolving after the Docker container was removed.

**Secondary:** SQLite WAL file not checkpointed. The main `db.sqlite3` was 4KB (empty). All live data was in `db.sqlite3-wal` (2.6MB). Backup scripts were copying only the main file, which would have produced silent incomplete backups.

**Contributing:** URL format error during reconnection. Entering `http://192.168.100.28:8096` in the hostname field and `8096` in the port field caused Jellyseerr to construct a malformed URL (`http://192.168.100.28:8096:8096`).

### Why it was not caught earlier

Jellyseerr appeared healthy until Jellyfin was removed from Docker. No monitoring existed on the Jellyfin connection status. The WAL backup gap was invisible because the main DB file existed and appeared valid.

### What changed as a result

1. Jellyseerr reconnected to baremetal Jellyfin using host LAN IP (`192.168.100.28:8096`)
2. WAL checkpoint procedure added to `backup-media.sh` — container is stopped, WAL is flushed, DB is copied, container is restarted
3. Architecture decision documented — Docker containers must always reference baremetal services by LAN IP, never `localhost` or Docker service hostname

### CISA domain mapping

| Domain | Relevance |
|--------|-----------|
| Domain 2 — IT Governance | No change management process for Jellyfin migration — Jellyseerr dependency was not identified or updated |
| Domain 4 — IS Operations and Business Resilience | Backup script covered the wrong file — WAL pattern was unknown, producing silently incomplete backups |
| Domain 5 — Protection of Information Assets | SQLite WAL behaviour must be accounted for in any backup procedure covering SQLite databases |

### Key principle reinforced

> SQLite WAL files hold live data. The main `.sqlite3` file is stale until a checkpoint occurs. Copying only the main file without stopping the container first is a silent backup failure.

---

## Incident 003 — DNS outage during Pi-hole network_mode migration

**Date:** 2026-06-11
**Severity:** Low
**Status:** Resolved

### What happened

Pi-hole was being migrated from `network_mode: host` to bridge networking to allow Caddy to route to it via the `traefik_proxy` Docker network. The old container was stopped before the replacement compose file had been created at the new path. This left port 53 unbound for several minutes, causing DNS resolution to fail across the network and briefly interrupting internet access.

### What was lost

- DNS resolution for approximately 3–5 minutes
- Internet access briefly interrupted (Tailscale fell back to its own DNS at 100.100.100.100)

### What survived

- All Pi-hole config and data (already copied to /opt/docker/pihole before the outage)
- All other services unaffected
- DNS recovered immediately once Pi-hole was restarted with the new compose file

### Root cause

**Primary:** No pre-staged compose file. The container was stopped before the replacement compose file existed at the new path, creating an unnecessary outage window.

**Secondary:** `network_mode: host` containers cannot be hot-attached to Docker bridge networks. The migration required a full stop/reconfigure/start cycle with no zero-downtime path available.

**Contributing:** The `docker network connect` attempt revealed the limitation only after the container was already down, extending the outage while the compose file was written from scratch.

### Why it was not caught earlier

The network_mode limitation was not known before attempting the migration. The assumption was that `docker network connect` would work as it does for standard bridge containers.

### What changed as a result

1. Pi-hole successfully migrated to `/opt/docker/pihole` with bridge networking
2. Compose file now version-controlled at new location
3. Port 53 mapped explicitly — DNS survives container restarts
4. `--accept-dns=false` flag noted for Tailscale to prevent it overriding Pi-hole DNS

### Key principle reinforced

> For DNS and other critical network services, always write and verify the replacement compose file before stopping the running service. The outage window is the gap between stop and start — eliminate it before you pull the trigger.

### CISA domain mapping

| Domain | Relevance |
|--------|-----------|
| Domain 2 — IT Governance | No pre-migration checklist for services with network_mode constraints — limitation discovered at runtime |
| Domain 4 — IS Operations and Business Resilience | Critical DNS service had no warm standby — single point of failure exposed during planned maintenance |

---

## Incident 004 — Caddy Caddyfile never persisted to disk or version control

**Date:** 2026-06-16
**Severity:** Medium
**Status:** Resolved

### What happened

After Caddy was deployed and configured to route 14 services via HTTPS on *.danlab, reports emerged that services appeared to be losing settings and configurations. Investigation revealed no actual data loss had occurred. The root cause was that Caddy was running from cached internal state with an empty Caddyfile on disk — meaning any container recreate would have permanently destroyed the entire reverse proxy routing configuration with no runtime recovery path available.

### What was lost

- Nothing permanently. All service data and bind mounts were intact.
- Caddy routing config was at risk — one container recreate away from total loss.

### What survived

- All 14 service routes (Caddy was running from cached data/state)
- All service bind mounts and data directories
- All TLS certificates (stored in /opt/docker/caddy/data/)

### Root cause

**Primary:** The Caddyfile was never written to disk at the bind mount path. Caddy started successfully on first run by generating its config internally, and the empty host file was never caught because the service appeared healthy.

**Secondary:** Caddy's admin API was disabled (`admin off` in the global block), eliminating the only runtime recovery path. With the API off, there is no way to extract the live config from a running container.

**Contributing:** The Caddyfile was never committed to Git and the homelab repo had no configured remote — meaning even if the file had existed on disk, it had no offsite protection.

### Why it was not caught earlier

Caddy appeared fully healthy — all 14 services were routing correctly via HTTPS. The empty Caddyfile on disk was invisible because the service never reported an error. The state inventory noted Caddy as fully covered but the Caddyfile path had not been verified to contain actual content.

### What changed as a result

1. Caddyfile reconstructed from scratch and saved to `/opt/docker/caddy/config/Caddyfile`
2. Caddyfile committed to Git at `infrastructure/caddy/Caddyfile`
3. Caddy added to `backup-infra.sh` staging — Caddyfile and docker-compose.yml now backed up to Restic and Google Drive nightly
4. Homelab Git repo connected to remote at https://github.com/cyberbydan/homelab and fully pushed for the first time
5. State inventory updated — admin API limitation documented in Caddy notes

### Key principle reinforced

> A service that appears healthy is not the same as a service that is recoverable.
> Verify that config files actually contain content, not just that the bind mount path exists.
> A bind mount pointing to an empty file is silent misconfiguration.

### CISA domain mapping

| Domain | Relevance |
|--------|-----------|
| Domain 2 — IT Governance | No verification step after Caddy deployment confirmed config was persisted to disk |
| Domain 4 — IS Operations and Business Resilience | Admin API disabled with no alternative recovery path — single point of failure in routing config |
| Domain 5 — Protection of Information Assets | Critical routing config existed only in container runtime state with no backup or version control |

---

## Incident 005 — n8n compose file lost, database lost on container recreate

**Date:** 2026-06-17
**Severity:** Medium
**Status:** Resolved

### What happened

During Session 5, the n8n HTTP Request node was timing out when calling the Flask API. Debugging revealed that n8n is containerised and UFW was blocking Docker traffic from reaching Flask on port 5050. As part of the investigation, the n8n container was force-recreated. This exposed two gaps: the compose file no longer existed at `~/homelab/infrastructure/` (lost in a previous restructure), and `database.sqlite` was not in the bind-mounted volume — it had been stored in the container's internal filesystem and was never written to the host.

### What was lost

- n8n `database.sqlite` — all workflow state, execution history, credentials
- n8n compose file at `~/homelab/infrastructure/docker-compose.yml`

### What survived

- `workflows-export.json` at `~/homelab/infrastructure/n8n-data/` — all workflows recovered from this
- All backup scripts and Flask API — unaffected
- All other services — unaffected

### Root cause

**Primary:** UFW blocking Docker → host traffic. Docker containers do not originate from the LAN subnet (`192.168.100.0/24`), so the blanket ALLOW rule for that subnet did not cover them. Port 5050 had no explicit UFW rule.

**Secondary:** n8n compose file missing from disk. Lost during homelab directory restructure — was not committed to Git before the restructure.

**Contributing:** `database.sqlite` not in bind-mounted volume. The volume mount path existed but the database was being written to the container's internal filesystem. This is a repeat of Incident 001 — the bind mount was not verified.

### Why it was not caught earlier

The n8n container was running and all workflows functioned correctly. The missing compose file and unverified bind mount were invisible until the container was recreated.

### What changed as a result

1. UFW rule added: `sudo ufw allow 5050/tcp` — Docker containers can now reach Flask
2. n8n compose file recreated at `~/homelab/infrastructure/docker-compose.yml` with `extra_hosts: host.docker.internal:host-gateway`
3. Workflows restored from `workflows-export.json` via `n8n import:workflow` CLI
4. Telegram credential manually recreated
5. **n8n Auto Export workflow built** — exports all workflows to Git every 6 hours automatically, so this can never be a total loss again
6. UFW port 5050 documented as a required setup step for the Flask API

### CISA domain mapping

| Domain | Relevance |
|--------|-----------|
| Domain 2 — IT Governance | Compose file not committed to Git before restructure — no change management process enforced |
| Domain 4 — IS Operations and Business Resilience | Bind mount unverified — repeat of Incident 001 pattern |
| Domain 5 — Protection of Information Assets | Credentials stored only in n8n database with no independent backup |

### Key principle reinforced

> UFW on a Docker host requires explicit rules for each port that containers need to reach on the host. The LAN subnet ALLOW rule does not cover Docker bridge traffic.
> Always verify bind mounts are receiving writes before relying on them for state.

---

## Incident index

| ID | Date | Service | Severity | Summary | Status |
|----|------|---------|----------|---------|--------|
| 001 | June 2026 | n8n | Medium | Workflow and credential loss due to unverified bind mount | Resolved |
| 002 | 2026-06-07 | Jellyseerr | Medium | Data recovery after Jellyfin Docker→baremetal migration | Resolved |
| 003 | 2026-06-11 | Pi-hole / DNS | Low | DNS outage during network_mode:host → bridge migration | Resolved |
| 004 | 2026-06-16 | Caddy | Medium | Caddyfile never persisted to disk — routing config one recreate away from total loss | Resolved |
| 005 | 2026-06-17 | n8n | Medium | Compose file lost, database lost on container recreate, UFW blocking Docker→Flask | Resolved |