# Session 5 — Plan and Context

Last updated: 2026-06-16
Maintained by: Dan Isaaka

---

## Context — What exists already

### Flask Backup API
n8n cannot run shell commands directly (Execute Command node removed in newer versions for security).
The workaround is a small Flask API running on the host that n8n calls via HTTP Request node.
The API runs the backup scripts and returns JSON results.

- **File:** `~/homelab/scripts/backup-api.py`
- **Runs as:** systemd service — starts on boot
- **Base URL:** `http://192.168.100.28:5050`
- **Endpoints:**
  - `POST /backup/infra` — runs backup-infra.sh, returns JSON result
  - `POST /backup/media` — runs backup-media.sh, returns JSON result (to be built)
  - `POST /backup/control-panel` — runs backup-control-panel.sh, returns JSON result (to be built)

### n8n Infrastructure Backup Workflow — COMPLETE
Already built and working. Runs daily at 2:00am.

**Node 1 — Schedule Trigger**
- Type: Schedule Trigger
- Interval: Daily at 02:00

**Node 2 — Run Backup**
- Type: HTTP Request
- Method: POST
- URL: `http://192.168.100.28:5050/backup/infra`
- Timeout: 600000ms (10 minutes)

**Node 3 — Build Message**
- Type: Code
- Mode: Run Once for All Items
```javascript
const data = $input.first().json;

const statusIcon = data.status === "success" ? "✅" : "⚠️";

const stepLines = [
  `${data.steps.authentik_db ? "🟢" : "🔴"} Authentik DB`,
  `${data.steps.restic ? "🟢" : "🔴"} Restic snapshot`,
  `${data.steps.rclone ? "🟢" : "🔴"} Google Drive`,
].join("\n");

const message = `${statusIcon} *Infrastructure Backup*\n` +
  `_${data.timestamp}_\n\n` +
  `${stepLines}\n\n` +
  `📦 Size: ${data.backup_size}\n` +
  `⏱ Duration: ${data.duration_seconds}s\n` +
  `🗄 Restic snapshots: ${data.restic_snapshots}` +
  (data.failed_steps ? `\n\n❌ Failed: ${data.failed_steps}` : "");

return [{ json: { message } }];
```

**Node 4 — Telegram**
- Type: Telegram
- Operation: Send Message
- Parse Mode: Markdown

---

## Session 5 — Priority Task List

### 1. Media stack backup workflow in n8n — FIRST PRIORITY
Mirror the infrastructure backup workflow for the media stack.

**What needs to happen:**
- Verify `/backup/media` endpoint exists in Flask API and returns correct JSON
- Build n8n workflow: Schedule → HTTP Request → Build Message → Telegram
- Schedule: Sunday 3:00am (matches backup-media.sh cron)
- The message should report: Sonarr DB, Radarr DB, Jellyseerr DB, Bazarr DB, Restic, Google Drive

**JSON response from backup-media.sh should include:**
- status, timestamp, duration_seconds, backup_size, restic_snapshots, failed_steps
- steps: sonarr, radarr, jellyseerr, bazarr, restic, rclone

Check current backup-media.sh to confirm it writes a JSON log like backup-infra.sh does.

### 2. Control panel backup workflow in n8n
Same pattern — Schedule → HTTP Request → Telegram.
Schedule: Daily at 2:30am (matches backup-control-panel.sh cron).

### 3. Uptime Kuma → Telegram notifications
When any monitor goes down, send a Telegram alert.
- Go to Uptime Kuma → Settings → Notifications → Add Telegram notification
- Need bot token and chat ID (already used in n8n workflows)
- Apply notification to all 16 monitors

### 4. Jellyfin TCP monitor timeout fix
Currently red in Uptime Kuma. Try:
- Increase timeout to 10 seconds
- Or switch to HTTP monitor on http://192.168.100.28:8096

### 5. Authentik SSO enforcement — SECURITY PRIORITY
Authentik is running but services are not protected behind it.
Anyone on the network can access Portainer, Grafana, n8n, code-server without auth.
Need to configure Caddy forward auth to enforce Authentik on sensitive services.

Services to protect behind SSO:
- Portainer
- Grafana
- n8n
- code-server
- Prowlarr
- qBittorrent

Services to leave open (or with lighter auth):
- Homepage
- Jellyfin
- Jellyseerr

### 6. n8n workflow export and backup verification
Workflows were lost in Incident 001. New workflows being built in Session 5 need to be:
- Exported to JSON immediately after creation
- Verified the export lands in backup staging
- Confirmed backup-infra.sh is picking them up

---

## Telegram Bot Context
- Bot token and chat ID are stored in `~/homelab/telegram-bots/.env`
- Already used in n8n Telegram nodes
- Superbot is the main bot — modular architecture, runs as systemd service
- Three bots total — all in `~/homelab/telegram-bots/`

---

## Infrastructure state going into Session 5

| Component | Status |
|-----------|--------|
| All 14 services | ✅ Running and monitored |
| Caddy routing | ✅ 14 services on *.danlab |
| Pi-hole DNS | ✅ All .danlab records active |
| Backups | ✅ All three scripts green |
| GitHub | ✅ Connected, all commits pushed |
| Uptime Kuma | ✅ 16 monitors, 15 green, Jellyfin TCP pending |
| n8n infra workflow | ✅ Built and working |
| n8n media workflow | ❌ Not built yet — Session 5 first task |
| n8n control panel workflow | ❌ Not built yet |
| Uptime Kuma notifications | ❌ Not configured yet |
| Authentik SSO enforcement | ❌ Not enforced — open access risk |

---

## Start Session 5 here

1. Check Flask API has `/backup/media` and `/backup/control-panel` endpoints
2. Check backup-media.sh writes a JSON log file like backup-infra.sh
3. Build media backup n8n workflow
4. Build control panel n8n workflow
5. Set up Uptime Kuma Telegram notifications
6. Fix Jellyfin TCP monitor
7. Plan Authentik SSO enforcement