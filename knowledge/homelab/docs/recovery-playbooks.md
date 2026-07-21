# Recovery Playbooks

This document contains step-by-step recovery procedures for each critical service in the homelab.
Each playbook defines what state exists, where it is backed up, and exactly how to restore it.

**Last updated:** 2026-06-17
**Maintained by:** Dan Isaaka

**Before running any playbook:** confirm you have a recent backup by checking the relevant JSON log:
- `~/homelab/backups/last-infra-backup.json`
- `~/homelab/backups/last-media-backup.json`
- `~/homelab/backups/last-control-panel-backup.json`

---

## General restore procedure

1. Identify the affected service
2. Stop the container: `docker compose -f ~/homelab/<stack>/docker-compose.yml down`
3. Confirm the backup exists and is recent
4. Follow the service-specific playbook below
5. Start the container and verify it is healthy
6. Update Uptime Kuma status if needed
7. Record the incident in `docs/lessons-learned.md`

---

## Playbook 001 — n8n

**Critical state:** workflows, credentials, execution history
**Backup location:** Restic repo → Google Drive (infra target)
**Backup frequency:** Daily via `backup-infra.sh` + every 6 hours via n8n Auto Export workflow
**Workflow exports:** `~/homelab/infrastructure/n8n-data/workflows-export.json`
**Credentials:** NOT in any backup — must be recreated manually from BotFather
**Estimated rebuild time (from backup):** 30 minutes
**Estimated rebuild time (from scratch):** 2–3 hours

### Before rebuilding — verify bind mount

This is the root cause of both Incident 001 and Incident 005. Do not skip this.

```bash
# Confirm bind mount path exists and has content
ls -la ~/homelab/infrastructure/n8n-data/

# Start container
docker compose -f ~/homelab/infrastructure/docker-compose.yml up -d n8n

# Write a test file from inside the container
docker exec n8n touch /home/node/.n8n/persistence-test.txt

# Confirm it appears on the host — MUST return the file
ls ~/homelab/infrastructure/n8n-data/persistence-test.txt

# Clean up test file
rm ~/homelab/infrastructure/n8n-data/persistence-test.txt
```

If the file does not appear on the host, stop. The bind mount is broken. Fix it before proceeding — otherwise you will lose state again on the next recreate.

### Restore workflows from JSON export

```bash
# Import all workflows
docker exec -it n8n n8n import:workflow \
  --input=/home/node/.n8n/workflows-export.json
```

### Recreate Telegram credential

- Go to `http://192.168.100.28:5678` → Settings → Credentials → Add credential
- Type: Telegram
- Name: `Telegram account`
- Token: get from BotFather → `/mybots` → select bot → API Token
- Save

### Restore from Restic (if JSON export is also missing)

```bash
restic -r ~/homelab/backups snapshots
restic -r ~/homelab/backups restore latest \
  --target /tmp/n8n-restore \
  --include /tmp/homelab-infra-staging/infrastructure/n8n
cp -r /tmp/n8n-restore/. ~/homelab/infrastructure/n8n-data/
docker compose -f ~/homelab/infrastructure/docker-compose.yml up -d n8n
```

### Post-restore checks

- [ ] n8n UI loads at `http://192.168.100.28:5678`
- [ ] All 5 workflows visible and active (Infra Backup, Media Backup, Control Panel Backup, n8n Auto Export, TEST-PERSISTENCE)
- [ ] Telegram credential present
- [ ] Run Infra Backup Report manually — confirm Telegram message arrives
- [ ] Confirm UFW allows port 5050: `sudo ufw status | grep 5050`

---

## Playbook 002 — Authentik

**Critical state:** users, groups, flows, application configs, provider configs
**Backup location:** Restic repo → Google Drive (infra target)
**Backup frequency:** Daily via `backup-infra.sh` (pg_dump)
**Estimated rebuild time (from backup):** 45 minutes
**Estimated rebuild time (from scratch):** 3–4 hours

### Restore from backup

```bash
docker compose -f ~/homelab/authentik/docker-compose.yml down

restic -r ~/homelab/backups restore latest \
  --target /tmp/authentik-restore \
  --include /tmp/homelab-infra-staging/authentik

docker compose -f ~/homelab/authentik/docker-compose.yml up -d authentik-db
docker exec -i authentik-db psql -U authentik authentik \
  < /tmp/authentik-restore/authentik/authentik-db.sql

docker compose -f ~/homelab/authentik/docker-compose.yml up -d
```

### Post-restore checks

- [ ] Authentik UI loads at `http://192.168.100.28:9300`
- [ ] Admin account accessible
- [ ] Applications and providers intact
- [ ] SSO login works for at least one downstream app

---

## Playbook 003 — Grafana

**Critical state:** dashboards, data source configs, alert rules
**Backup location:** Restic repo → Google Drive (infra target)
**Backup frequency:** Daily via `backup-infra.sh`
**Estimated rebuild time (from backup):** 20 minutes
**Estimated rebuild time (from scratch):** 1–2 hours

### Restore from backup

```bash
docker compose -f ~/homelab/infrastructure/docker-compose.yml down grafana

restic -r ~/homelab/backups restore latest \
  --target /tmp/grafana-restore \
  --include /tmp/homelab-infra-staging/infrastructure

cp -r /tmp/grafana-restore/. ~/homelab/infrastructure/

docker compose -f ~/homelab/infrastructure/docker-compose.yml up -d grafana
```

### Post-restore checks

- [ ] Grafana UI loads at `http://192.168.100.28:3000`
- [ ] Loki data source connected
- [ ] Dashboards visible and loading data

---

## Playbook 004 — Pi-hole

**Critical state:** custom DNS entries, allowlist/blocklist customizations
**Excluded from backup:** gravity database (rebuildable via `pihole -g`)
**Backup location:** Restic repo → Google Drive (infra target)
**Estimated rebuild time (from backup):** 15 minutes
**Estimated rebuild time (from scratch):** 20 minutes

### Restore config from backup

```bash
restic -r ~/homelab/backups restore latest \
  --target /tmp/pihole-restore \
  --include /tmp/homelab-infra-staging/pihole

cp -r /tmp/pihole-restore/. ~/pihole/

docker compose -f ~/pihole/docker-compose.yml up -d

# Rebuild gravity DB — this is normal, not a loss
docker exec pihole pihole -g
```

### Post-restore checks

- [ ] Pi-hole admin UI accessible
- [ ] DNS resolution working from a client device
- [ ] Custom DNS entries present
- [ ] Gravity update completed successfully

---

## Playbook 005 — Flask backup API

**Critical state:** `backup-api.py` source, systemd service file
**Backup location:** Git repository (primary), Restic (secondary)
**Estimated rebuild time:** 10 minutes

### Restore from Git

```bash
cd ~/homelab && git pull

pip3 install flask docker --break-system-packages

sudo cp ~/homelab/scripts/backup-api.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now backup-api
sudo systemctl status backup-api

# Confirm UFW rule is in place
sudo ufw status | grep 5050
# If missing: sudo ufw allow 5050/tcp

curl http://localhost:5050/health
```

### Post-restore checks

- [ ] Service running: `systemctl is-active backup-api`
- [ ] Health endpoint returns 200
- [ ] All status endpoints respond: `/backup/infra/status`, `/backup/media/status`, `/backup/control-panel/status`
- [ ] Docker containers can reach it: `docker exec n8n wget -qO- http://192.168.100.28:5050/health`

---

## Playbook 006 — Homepage

**Critical state:** YAML config files (services, settings, widgets)
**Backup location:** Restic repo → Google Drive (control-panel target)
**Backup frequency:** Daily via `backup-control-panel.sh`
**Estimated rebuild time (from backup):** 5 minutes
**Estimated rebuild time (from scratch):** 15 minutes

### Restore from backup

```bash
restic -r ~/homelab/backups restore latest \
  --target /tmp/cp-restore \
  --include /tmp/homelab-control-panel-staging/homepage/config

cp -r /tmp/cp-restore/. ~/homelab/control-plane/homepage/config/

docker compose -f ~/homelab/control-plane/homepage/docker-compose.yml up -d
```

### Post-restore checks

- [ ] Homepage loads at `http://192.168.100.28:3005`
- [ ] All service groups visible
- [ ] Status indicators showing green for running services

---

## Playbook 007 — Superbot

**Critical state:** source code, `.env` credentials
**Backup location:** Git (code only — `.env` excluded and never committed)
**Estimated rebuild time:** 10 minutes

### Restore from Git

```bash
cd ~/homelab && git pull

# Install dependencies
pip install -r ~/homelab/telegram-bots/requirements.txt --break-system-packages

# Recreate .env — tokens are not in Git
nano ~/homelab/telegram-bots/.env
```

Paste:
```
BOT_TOKEN=your_token_from_botfather
ALLOWED_USER=danisaaka
```

Get token from BotFather → `/mybots` → select Superbot → API Token.

```bash
# Reinstall and start systemd service
sudo cp ~/homelab/telegram-bots/superbot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now superbot
sudo systemctl status superbot
```

### Post-restore checks

- [ ] Service running: `systemctl is-active superbot`
- [ ] Send `/start` in Telegram — main menu appears
- [ ] System → Disk returns data
- [ ] Backups → Infrastructure returns last backup status
- [ ] Containers → list returns running containers
- [ ] Media → Active Downloads returns data or empty queue message

---

## Playbook 008 — Media stack databases

**Covers:** Sonarr, Radarr, Jellyseerr, Bazarr
**Backup location:** Restic repo → Google Drive (media target)
**Backup frequency:** Weekly Sunday 3:00am via `backup-media.sh`
**Estimated rebuild time (from backup):** 20 minutes

### Important — Jellyseerr WAL

Jellyseerr uses SQLite WAL mode. The backup script stops the container before copying to ensure the WAL is checkpointed. When restoring, always restore `jellyseerr.db` while the container is stopped.

### Restore individual DB

```bash
# Stop the affected container
docker stop sonarr  # or radarr, jellyseerr, bazarr

# Restore from latest media backup
restic -r ~/homelab/backups restore latest \
  --target /tmp/media-restore \
  --include /tmp/homelab-media-staging/databases

# Copy the specific DB back
cp /tmp/media-restore/databases/sonarr.db \
   ~/homelab/media/sonarr/sonarr.db

# Start container
docker start sonarr
```

### Post-restore checks

- [ ] Container starts healthy
- [ ] Library intact in UI
- [ ] Quality profiles and history present
- [ ] For Jellyseerr — requests visible, Jellyfin connection active

---

## Playbook 009 — Full homelab rebuild (bare metal)

Use this when the EliteBook itself is replaced or Ubuntu is reinstalled.

**Estimated time:** 4–6 hours

### Step 1 — Base system

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker dan-isaaka

sudo apt install -y restic rclone git python3-pip zsh sqlite3

sh -c "$(wget -O- https://install.ohmyz.sh)"
chsh -s /bin/zsh
```

### Step 2 — Restore homelab Git repo

```bash
git clone https://github.com/cyberbydan/homelab.git ~/homelab
```

### Step 3 — Restore from Google Drive

```bash
rclone sync gdrive:homelab-infra-backup /tmp/homelab-infra-restore
rclone sync gdrive:homelab-media-backup /tmp/homelab-media-restore
rclone sync gdrive:homelab-control-panel-backup /tmp/homelab-cp-restore
```

### Step 4 — UFW setup

```bash
sudo ufw allow 22/tcp
sudo ufw allow 5050/tcp    # Flask API — required for Docker containers
sudo ufw allow from 192.168.100.0/24
sudo ufw enable
```

### Step 5 — Start services in dependency order

```bash
# 1. Pi-hole (DNS must come first)
docker compose -f /opt/docker/pihole/docker-compose.yml up -d

# 2. Caddy (after DNS)
docker compose -f /opt/docker/caddy/docker-compose.yml up -d

# 3. Authentik
docker compose -f ~/homelab/authentik/docker-compose.yml up -d

# 4. Monitoring stack
docker compose -f ~/homelab/loki-stack/docker-compose.yml up -d

# 5. Infrastructure stack (n8n, Portainer, Grafana, code-server)
docker compose -f ~/homelab/infrastructure/docker-compose.yml up -d

# 6. Control plane (Homepage)
docker compose -f ~/homelab/control-plane/homepage/docker-compose.yml up -d

# 7. Media stack
docker compose -f ~/homelab/media/docker-compose.yml up -d
```

### Step 6 — Restore systemd services

```bash
sudo cp ~/homelab/scripts/backup-api.service /etc/systemd/system/
sudo cp ~/homelab/telegram-bots/superbot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now backup-api superbot
```

### Step 7 — Recreate .env files (not in Git)

```bash
# Superbot
nano ~/homelab/telegram-bots/.env
# BOT_TOKEN=get from BotFather
# ALLOWED_USER=danisaaka
```

### Step 8 — Restore n8n workflows

Follow Playbook 001.

### Step 9 — Confirm Tailscale

```bash
sudo tailscale up
tailscale status
```

### Step 10 — Verify each service

Run through each playbook above for the services that hold critical state.

---

## Restore drill log

Run one restore drill per month. Pick any non-critical service, destroy its volume, restore from backup, and record the result here.

| Date | Service | Method | Result | Time taken | Notes |
|------|---------|--------|--------|------------|-------|
| — | — | — | — | — | No drills run yet |

---

## Quick reference

| Service | Backup type | RTO (from backup) | RTO (from scratch) | Critical state |
|---------|-------------|-------------------|--------------------|----------------|
| n8n | Restic + JSON export (6hr) | 30 min | 2–3 hrs | Workflows — credentials need manual recreate |
| Authentik | Restic (pg_dump) | 45 min | 3–4 hrs | Users, flows, apps |
| Grafana | Restic | 20 min | 1–2 hrs | Dashboards, sources |
| Pi-hole | Restic (config only) | 15 min | 20 min | Custom DNS entries |
| Flask API | Git | 10 min | 10 min | Source code |
| Homepage | Restic | 5 min | 15 min | YAML configs |
| Superbot | Git + manual .env | 10 min | 10 min | Source code, tokens |
| Media DBs | Restic (weekly) | 20 min | rebuild | Sonarr/Radarr/Jellyseerr/Bazarr DBs |
| Full rebuild | Restic + Git | 4–6 hrs | 8+ hrs | Everything |