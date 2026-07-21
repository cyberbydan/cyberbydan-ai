# Session 5 — Notes and Outcomes

**Date:** 2026-06-17
**Maintained by:** Dan Isaaka
**Duration:** Full session
**Status:** Complete

---

## What We Set Out To Do

1. Media stack backup workflow in n8n
2. Control panel backup workflow in n8n
3. Uptime Kuma Telegram notifications
4. Jellyfin TCP monitor timeout fix
5. Authentik SSO enforcement
6. n8n workflow export and backup verification

---

## What Actually Happened

### 1. backup-media.sh — Patched

The original script only tracked `restic` and `rclone` in the JSON output. Individual DB copies (Sonarr, Radarr, Jellyseerr, Bazarr) were silently failing with no visibility.

**Fix:** Added per-step exit code tracking for all 5 databases. JSON output now includes:
```json
"steps": {
  "sonarr": true,
  "radarr": true,
  "jellyseerr": true,
  "bazarr": true,
  "restic": true,
  "rclone": true
}
```

Prowlarr is backed up but intentionally excluded from overall status — it's indexer config, not critical library data. Documented in script comments.

Jellyseerr requires a WAL checkpoint before copy — container is stopped, WAL flushed, DB copied, container restarted. This is correct and intentional.

---

### 2. backup-control-panel.sh — Patched

Added tracking for `homepage_config` step — the `cp -r` of the config folder was previously silent. Now tracked and included in JSON and Telegram message.

```json
"steps": {
  "homepage_config": true,
  "restic": true,
  "rclone": true
}
```

---

### 3. n8n Workflows — Restored and Rebuilt

**Root cause of session complexity:** n8n compose file was lost in Incident 001. The container was still running from its last start but had no compose file on disk. When we recreated it, it started fresh with an empty database.

**Recovery:** Workflows were restored from `workflows-export.json` via CLI import.

**New issue discovered:** n8n is containerised. It cannot reach Flask (running on host) via `192.168.100.28` because UFW was blocking Docker traffic — Docker traffic doesn't originate from the LAN subnet so the blanket `192.168.100.0/24 ALLOW` rule didn't cover it.

**Fix:** `sudo ufw allow 5050/tcp`

This should be documented as a required step when setting up the Flask API on any new host.

**n8n compose file** recreated at `~/homelab/infrastructure/docker-compose.yml` with `extra_hosts: host.docker.internal:host-gateway` added (not strictly needed now that UFW is open, but correct to have).

All three workflows restored and tested:
- ✅ Infra Backup Report — daily 2:05am
- ✅ Media Stack Backup — Sunday 3:05am
- ✅ Control Panel Backup Report — daily 2:35am

---

### 4. Telegram Messages — Redesigned

All three workflows got a new message format. Key improvements:
- Day name derived from timestamp
- Fixed step order regardless of JSON key order
- Stats line: size · duration · snapshots
- Next run reminder
- Failed steps callout with ⛔ icon
- 🟢/🔴 dots instead of ✅/❌ for steps

---

### 5. n8n Auto Export Workflow — Built

**Problem:** Workflows were lost in Incident 001 because exports weren't automatic.

**Solution:** New workflow — `n8n Auto Export` — runs every 6 hours:
1. Calls n8n internal API (`GET localhost:5678/api/v1/workflows`) with API key auth
2. Formats response with timestamp and workflow count
3. POSTs to new Flask endpoint `/git/export-and-commit`
4. Flask writes JSON to `~/homelab/infrastructure/n8n-data/workflows-export.json`
5. Flask runs `git add → git commit → git push`

Note: n8n must call its own API via `localhost`, not `host.docker.internal` — calling itself via the external hostname causes a loop.

New Flask endpoint added to `backup-api.py`:
- `POST /git/export-and-commit`

---

### 6. Superbot V2 — Rebuilt from Scratch

Previous superbot files were lost in homelab restructure. Rebuilt with a proper modular architecture.

**Structure:**
```
~/homelab/telegram-bots/
├── superbot.py              # entry point
├── .env                     # token + allowed user (not in git)
├── requirements.txt
├── superbot-architecture.md
└── modules/
    ├── __init__.py
    ├── system.py            # disk, RAM, uptime, health
    ├── backups.py           # status for all three decks
    ├── containers.py        # list running containers
    └── media.py             # Sonarr/Radarr queues, active downloads
```

**Key decisions:**
- Media module calls Sonarr/Radarr directly — their queue APIs are richer than Flask
- Silent auth reject — unknown users get no response
- All navigation via inline keyboards — no slash commands beyond /start and /menu
- Runs as systemd service — persistent, restarts on crash, starts on boot

**Running as:** `superbot.service` — installed to `/etc/systemd/system/`

---

## Items Deferred to Session 6

| Item | Notes |
|------|-------|
| Uptime Kuma Telegram notifications | Need bot token and chat ID configured in Kuma |
| Jellyfin TCP monitor fix | Try increasing timeout or switching to HTTP monitor |
| Authentik SSO enforcement | Bigger lift — needs Caddy forward auth config planned first |

---

## Incidents and Discoveries

### UFW blocking Docker → Flask
Docker containers cannot reach host services via LAN IP if UFW is active and doesn't explicitly allow the port. The `192.168.100.0/24 ALLOW` rule only covers LAN traffic, not Docker bridge traffic.

**Resolution:** `sudo ufw allow 5050/tcp`
**Lesson:** Any Flask API port needs an explicit UFW rule when n8n or other containers need to reach it.

### n8n compose file missing
The live container was running but had no compose file on disk — lost in Incident 001. Container survived a reboot but any `docker compose` command failed.

**Resolution:** Recreated compose file from the archive copy at `~/homelab/archive/homelab-fix-20260607/infrastructure/docker-compose.yml`.
**Lesson:** Compose files must be committed to git immediately after creation. The auto-export workflow now handles n8n workflows — compose files still need manual discipline.

### n8n database lost
When the container was force-recreated, it started fresh because `database.sqlite` wasn't in the mounted volume — it had been stored elsewhere and lost.

**Resolution:** Restored from `workflows-export.json` via `n8n import:workflow` CLI. Credentials had to be manually recreated.
**Lesson:** The auto-export workflow now runs every 6 hours. Credentials cannot be exported — store the Telegram bot token in `~/homelab/telegram-bots/.env` and ensure that file is backed up separately.

---

## Infrastructure State After Session 5

| Component | Status |
|-----------|--------|
| All services | ✅ Running |
| backup-media.sh | ✅ Patched — 6 steps tracked |
| backup-control-panel.sh | ✅ Patched — 3 steps tracked |
| n8n infra workflow | ✅ Running — daily 2:05am |
| n8n media workflow | ✅ Running — Sunday 3:05am |
| n8n control panel workflow | ✅ Running — daily 2:35am |
| n8n auto export | ✅ Running — every 6 hours |
| Superbot | ✅ Running as systemd service |
| UFW port 5050 | ✅ Open |
| Uptime Kuma notifications | ❌ Deferred to Session 6 |
| Jellyfin TCP monitor | ❌ Deferred to Session 6 |
| Authentik SSO enforcement | ❌ Deferred to Session 6 |

---

## Start Session 6 Here

1. Uptime Kuma → Settings → Notifications → Add Telegram
   - Bot token from BotFather
   - Chat ID: 255234922
   - Apply to all 16 monitors
2. Fix Jellyfin TCP monitor — increase timeout to 10s or switch to HTTP on port 8096
3. Plan Authentik SSO enforcement — Caddy forward auth for Portainer, Grafana, n8n, code-server, Prowlarr, qBittorrent
4. Superbot V3 planning — move API keys to .env, add backup triggers, Jellyseerr module
