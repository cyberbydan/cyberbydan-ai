# Session 6 — Notes and Outcomes

**Date:** 2026-06-29 to 2026-06-30
**Maintained by:** Dan Isaaka
**Duration:** Full session (spanned two days)
**Status:** Complete

---

## What We Set Out To Do

1. Connect Storm (Windows 11 Pro gaming PC) to the homelab ecosystem
2. Deploy Ollama + Open WebUI on Storm
3. Add DNS records and Homepage entries for Storm services
4. Migrate the full media stack from Elitebook to Storm
5. Set up Git on Storm
6. Update Homepage with Storm resource monitoring

---

## What Actually Happened

### 1. Storm joined Tailscale

Straightforward — Storm connected to the tailnet at `100.118.211.39`. This unlocked everything else.

---



### 2. Ollama + Open WebUI deployed

**Ollama:** installed natively on Windows for direct GPU access (RTX 3060). Required setting `OLLAMA_HOST=0.0.0.0` as a system environment variable so Docker containers could reach it via `host.docker.internal` — default is `127.0.0.1` only.

**Open WebUI:** deployed via Docker Desktop. First attempt failed because the compose file didn't exist where we thought — had to recreate it directly via PowerShell heredoc.

**Docker Desktop wouldn't start at all** — root cause was that Dan had disabled Windows driver signature enforcement to run pirated games, which silently broke Hyper-V. Fixed by:

```powershell
bcdedit /set testsigning off
bcdedit /set nointegritychecks off
bcdedit /set hypervisorlaunchtype auto
dism.exe /online /enable-feature /featurename:Microsoft-Hyper-V /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /norestart
```

Secure Boot actually blocked the testsigning/nointegritychecks flags from being set (which was correct — bypass was already partially neutralized). After a clean restart, Hyper-V came back and Docker started normally.

**This is now a known constraint:** Storm cannot run certain bypass-dependent games and Docker Desktop simultaneously. Flagged as a pending item for a future session — not solved yet, just identified and worked around for this session.

---



### 3. Tailscale DNS was broken — discovered and fixed

Dan reported that turning on Tailscale on any device other than the Elitebook killed internet access. Root cause was two-layered:

1. Pi-hole's listening mode was `LOCAL` — only accepts DNS from subnets with a matching local interface. Tailscale's point-to-point `/32` interface doesn't qualify, so Pi-hole silently dropped every query arriving over Tailscale.
2. Even after fixing the listening mode, UFW's LAN subnet rule didn't cover Docker bridge traffic from Tailscale IPs — needed explicit iptables rules.

**Fix:**

```bash
docker exec pihole pihole-FTL --config dns.listeningMode ALL
docker restart pihole
sudo iptables -I DOCKER-USER -s 100.64.0.0/10 -j ACCEPT
sudo iptables -I INPUT -s 100.64.0.0/10 -p udp --dport 53 -j ACCEPT
sudo iptables -I INPUT -s 100.64.0.0/10 -p tcp --dport 53 -j ACCEPT
sudo apt install iptables-persistent -y
sudo netfilter-persistent save
```

Verified working on Storm and on Dan's phone — internet and `.danlab` resolution both restored network-wide.

---



### 4. Full media stack migrated to Storm

This was the bulk of the session. Sequence:

1. Triggered a manual `backup-media.sh` run on the Elitebook before touching anything
2. Built `docker-compose.yml` on Storm covering Sonarr, Radarr, Lidarr, Prowlarr, Bazarr, Jellyseerr, qBittorrent, FlareSolverr, Navidrome
3. Copied databases from Elitebook to Storm — SCP failed (no SSH server on Storm), fell back to a Python HTTP server on the Elitebook + `Invoke-WebRequest` on Storm
4. Discovered two DB path mistakes during export: Jellyseerr's real DB is at `db/db.sqlite3` not `jellyseerr.db`, and Bazarr has two DB files (`bazarr.db` and `db/bazarr.db`) — used the wrong one initially
5. Moved DBs into place on Storm, had to `docker compose down` first since the fresh containers had already created empty DBs that blocked the move
6. Brought the stack up — all libraries (Sonarr, Radarr, Lidarr) loaded correctly. qBittorrent came up fresh (acceptable — no critical state)
7. Stopped and disabled the media stack and Jellyfin on the Elitebook
8. Installed Jellyfin bare metal on Storm for direct GPU transcoding access

**Indexer reconnection was the hardest part.** Prowlarr's own stored URLs still referenced old Elitebook container names (`prowlarr:9696`, `radarr:7878`, `sonarr:8989`). The "Sync App Indexers" button didn't overwrite existing indexer URLs in Sonarr/Radarr/Lidarr — had to delete all indexers in each app and re-sync from scratch after correcting Prowlarr's own server URL and each app's URL to `host.docker.internal`.

---



### 5. Caddy and Pi-hole config path corrections discovered

Two separate "editing the wrong file" incidents:

**Pi-hole:** `custom.list` is not Pi-hole v6's real config source — `pihole.toml` is. All `custom.list` edits had zero effect. DNS records had to be added via the admin UI instead, which correctly writes to `pihole.toml`.

**Caddy:** the Caddyfile actually mounted into the container is at `/opt/docker/caddy/config/Caddyfile`, not `~/homelab/infrastructure/caddy/Caddyfile` as the architecture doc claimed. Edits to the documented path did nothing. Also discovered the admin API being disabled means `caddy reload` fails outright — a full `docker restart caddy` is required for any config change.

**Homepage** had the same issue — real config is at `~/homelab/services/infra/homepage/config/`, not `~/homelab/control-plane/homepage/config/`. This cost real time mid-session before being caught via `docker inspect`.

**New engineering principle adopted:** always verify the real mounted path with `docker inspect <container> | grep -A20 Mounts` before editing a config file, regardless of what the docs say.

---



### 6. Storm Windows Firewall blocking cross-host Caddy proxy

After fixing the Caddyfile, media `.danlab` URLs still 502'd. Root cause: Storm's Windows Firewall had no inbound rules for the media service ports, so Caddy on the Elitebook couldn't reach them over Tailscale even though the services were running fine locally.

**Fix:** added inbound allow rules for all relevant ports (8989, 7878, 9696, 6767, 8080, 5055, 8686, 4533, 8191, 8096, 3000).

**Discovered a second issue afterward — hairpin routing.** When Storm itself tried to load `sonarr.danlab`, the request resolved to Storm's own Tailscale IP, hit Caddy on the Elitebook, which proxied back to Storm — and failed unpredictably. Fixed with a local Windows `hosts` file override mapping all Storm-hosted `.danlab` domains to `127.0.0.1`, so Storm always hits its own services directly and skips Caddy entirely for its own traffic.

---



### 7. Git set up on Storm

Installed Git, cloned the existing `cyberbydan/homelab` repo to `C:\homelab`. Added a new `storm/` folder containing Storm's docker-compose files, committed and pushed. Elitebook had a stale local branch from Storm's earlier push — resolved with `git stash` → `git pull --rebase` → `git stash pop` → `git push`.

---



### 8. Homepage rebuilt with Glances monitoring

Wanted CPU/RAM/GPU/disk stats for both machines on the dashboard. Installed Glances on Storm via pip, ran into a Python version mismatch (Glances running under 3.13, `pip install fastapi` initially went to a different interpreter) — fixed by calling pip explicitly through the same Python binary Glances uses. Wrapped Glances as a Windows service with NSSM so it survives reboots.

Rebuilt `services.yaml`, `widgets.yaml`, and `settings.yaml` from scratch — original file still had Homepage's default placeholder groups ("My First Group" etc.) untouched since initial setup. New config uses direct IP:port links (not `.danlab`) to sidestep the Storm hairpin issue, organized into a clean row-based grid layout.

---



### 9. Bazarr and Navidrome follow-up fixes

**Bazarr:** Sonarr/Radarr connections initially failed with a 401 — root cause was a typo'd leading space in the Host field (`' host.docker.internal'`). Rather than debug the migrated config further, rebuilt Bazarr's Sonarr/Radarr/provider config from scratch.

**Navidrome:** library only showing one album. Root cause identified but not yet fixed — the docker-compose volume maps `D:\media\music`, but Dan's actual media lives on `E:\media\music`. Same root cause affects qBittorrent's download path. Fix is queued for next session (find/replace `D:\media` → `E:\media` in the compose file, recreate containers).

---



## Items Deferred to Session 7


| Item                               | Notes                                                                            |
| ---------------------------------- | -------------------------------------------------------------------------------- |
| backup-storm.sh                    | **Most urgent** — Storm has zero backup coverage for the entire AI + media stack |
| D:\ vs E:\ path fix                | Lidarr, Navidrome, qBittorrent all affected — incomplete library scans           |
| Uptime Kuma Telegram notifications | Carried over from Session 5, still not done                                      |
| Authentik SSO enforcement          | Carried over from Session 5                                                      |
| Gaming + Docker coexistence        | Identified this session, not solved — Dan wants to keep gaming on Storm          |
| Superbot V3                        | Backup triggers, .env migration                                                  |
| Superbot V4                        | Now unblocked — Ollama is live, architecture is ready                            |
| Retire or repoint backup-media.sh  | Currently backs up nothing since media left the Elitebook                        |


---



## Incidents and Discoveries



### Driver signature enforcement bypass breaks Docker Desktop

Disabling Windows driver signature enforcement (commonly done to run pirated games with unsigned kernel drivers) silently disables Hyper-V, which Docker Desktop depends on for WSL2. Symptom was Docker Desktop hanging indefinitely on "Starting the Docker Engine."

**Resolution:** re-enable Hyper-V via DISM, set `hypervisorlaunchtype auto`, restart.
**Lesson:** these two use cases are fundamentally in tension on the same Windows installation. Needs a structural solution (dual boot, WSL2-native Docker, or accepting the tradeoff) — not yet decided.

### Pi-hole v6 config source confusion

`custom.list` is not authoritative in Pi-hole v6 — `pihole.toml` is, and it's edited correctly only via the admin UI or `pihole-FTL --config`. Significant time lost editing a file that had no effect.

**Resolution:** documented the real config source. All future Pi-hole DNS changes go through the admin UI.
**Lesson:** verify config file authority for any service before assuming docs (even Anthropic-authored docs from a previous session) are accurate.

### Caddy and Homepage real config paths didn't match documentation

Both services had drifted from their documented paths at some point before this session — likely during the `services/` folder restructure mentioned in earlier changelogs, which wasn't fully propagated to all docs.

**Resolution:** `docker inspect <container> | grep -A20 Mounts` is now the standard first step before editing any container's config.
**Lesson:** documentation drift is real and silent. Trust the running container over the docs when there's any doubt.

### Tailscale DNS killing internet access network-wide

Not migration-related, but discovered and fixed mid-session. Pi-hole's `LOCAL` listening mode silently dropped all Tailscale-origin DNS queries, which — combined with Tailscale's global nameserver setting — meant any device with Tailscale active lost internet entirely the moment it connected.

**Resolution:** `dns.listeningMode ALL` + explicit iptables rules for the Tailscale CIDR.
**Lesson:** Tailscale's MagicDNS global nameserver feature has a hard dependency on the DNS server actually accepting traffic from the tailnet's virtual interface — this isn't automatic and isn't obviously flagged anywhere in Tailscale's own UI.

---



## Infrastructure State After Session 6


| Component                                | Status                                               |
| ---------------------------------------- | ---------------------------------------------------- |
| Storm — Tailscale                        | ✅ Connected, 100.118.211.39                          |
| Storm — Ollama                           | ✅ Running, GPU accelerated                           |
| Storm — Open WebUI                       | ✅ Running                                            |
| Storm — Docker Desktop                   | ✅ Running (after Hyper-V fix)                        |
| Storm — full media stack                 | ✅ Running — indexers reconnected, downloads working  |
| Storm — Jellyfin                         | ✅ Running bare metal, GPU transcoding ready          |
| Storm — Glances                          | ✅ Running as Windows service                         |
| Storm — Git                              | ✅ Installed, repo cloned, pushing successfully       |
| Storm — backups                          | ❌ None — most urgent gap                             |
| Elitebook — media stack                  | ✅ Stopped and disabled (intentional)                 |
| Elitebook — Caddy                        | ✅ Running, proxying to both hosts                    |
| Elitebook — Pi-hole                      | ✅ Running, listening mode ALL, Tailscale DNS fixed   |
| Elitebook — Homepage                     | ✅ Rebuilt, showing both hosts                        |
| Lidarr/Navidrome/qBittorrent media paths | ⚠️ D:\ vs E:\ mismatch — pending fix                 |
| Bazarr                                   | ✅ Reconfigured fresh, needs provider re-verification |
| Uptime Kuma notifications                | ❌ Still deferred from Session 5                      |
| Authentik SSO enforcement                | ❌ Still deferred from Session 5                      |
| Gaming + Docker coexistence              | ❌ Identified, not solved                             |


---



## Start Session 7 Here

1. Fix D:\ vs E:\ media path mismatch in Storm's docker-compose.yml — affects Lidarr, Navidrome, qBittorrent
2. Design and build `backup-storm.sh` (or PowerShell equivalent) — this is the top priority, Storm currently has zero recovery path
3. Decide what to do with `backup-media.sh` on the Elitebook — it now backs up nothing
4. Re-verify Bazarr's 5 subtitle providers are correctly configured after the from-scratch rebuild
5. Revisit Uptime Kuma Telegram notifications (3rd session this has been deferred)
6. Plan a gaming + Docker coexistence strategy for Storm

