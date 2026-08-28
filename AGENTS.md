# AGENTS.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

AutoChess Fullstack is a modular auto-battler game built as a Git submodule monorepo. Submodules span an admin panel, two Rust backend services, a Godot game client, and a website placeholder.

```
Admin-Area/Admin-Panel/        # Laravel 12 (PHP 8.2) - fleet management, secrets, pairing
Backend/Backend-General/       # Rust (tokio/axum/tonic) - players, auth, matchmaking, WebSocket hub, gRPC server
Backend/Backend-Simulation/    # Rust (tokio/axum/tonic) - match engine, combat, shop, rounds, synergies
Frontend/Game-Client/          # Godot 4.x (GDScript) - visual client, WebSocket consumer, replay playback
Frontend/Game-Website/         # Placeholder (not yet implemented)
```

## Common Commands

### Full Stack (Docker)
```bash
cp .env.example .env          # first time only
docker compose up -d --build  # start postgres, redis, admin-panel+nginx, backend-general, backend-match
docker compose ps             # check service health
docker compose logs -f        # follow all logs
docker compose down           # stop; add -v to destroy DB/Redis volumes
```

See `INSTALL.md` for the full first-time setup flow (env vars, migration/seeding, push-based pairing, default admin login).

Default Admin Panel login (after `db:seed --class=InitialSetupSeeder`):
- Email: `admin@autochess.local`
- Password: `<set by seeder - change immediately after first login>`

### Service Ports (docker-compose)
| Service | Port | Notes |
|---------|------|-------|
| Admin Panel (nginx) | 3001 | Laravel interface |
| Backend General | 8081 (HTTP) / 50051 (gRPC) | REST + WS + gRPC server |
| Backend Match (Simulation) | 8082 | Match/combat engine |
| PostgreSQL | 5432 | `admin_panel` + `autochess` DBs |
| Redis | 6379 | Matchmaking queue / caching |

### Admin Panel (Laravel)
```bash
cd Admin-Area/Admin-Panel
docker compose exec admin-panel php artisan migrate --force
docker compose exec admin-panel php artisan db:seed --class=InitialSetupSeeder --force
docker compose exec admin-panel php artisan test          # run all tests
docker compose exec admin-panel php artisan test --filter=ClassName    # single test class
docker compose exec admin-panel php artisan key:generate   # regenerate APP_KEY
```

### Backend General (Rust)
```bash
cd Backend/Backend-General
cargo run                           # standalone (needs pairing.json or env vars)
cargo test                          # run tests
```

### Backend Simulation (Rust)
```bash
cd Backend/Backend-Simulation
cargo run                           # standalone
cargo test                          # run all tests
cargo test --package engine -- --nocapture  # single test with output
```

### Game Client
Open `Frontend/Game-Client/` in Godot Editor. See `PROGRESS.MD` for setup instructions.

## Architecture

### Service Communication
```
Game-Client ──WebSocket──► Backend-General (REST + WS hub + gRPC server)
                                │ gRPC
                                ▼
                          Backend-Simulation (match engine, deterministic combat)
                                │ HTTP heartbeat/config
                                ▼
                          Admin-Panel (Laravel, port 3001 via nginx)
```

- **Backend-General ↔ Backend-Simulation**: gRPC on port 50051. General exposes `MatchNotification` service; Simulation calls it when matches finish.
- **Game-Client → Backend-General**: WebSocket at `/ws` for real-time matchmaking, state sync. REST at `/api/auth/*` for login/register.
- **Admin-Panel → Backends**: HTTP POST to `/api/v1/pair` (push credentials), periodic heartbeats to `/api/v1/instances/heartbeat`, config export at `/api/v1/instances/export`.

### Push-Based Pairing
Backends start unpaired. Admin Panel pushes `pairing_key` + `admin_url` → backend writes `pairing.json`. On startup, backends fetch remote config from the Admin Panel's export endpoint using their pairing key. Heartbeats run every 30s.

### Config Resolution Order (Rust backends)
1. Environment variables (`.env` or OS)
2. Local `pairing.json` (overrides Admin URL and instance key)
3. Remote Admin Panel export (overrides all other secrets)

Backends support `CREDS_MANAGER_URL`, `CREDS_MANAGER_AUTH_KEY`, and `CREDS_MANAGER_SCOPES` (e.g. `Shared,general`) env vars to fetch secret groups from the Admin Panel export endpoint.

### Admin-Panel (Laravel)
- `app/Models/Instance` — Backend instances (name, type, endpoint, pairing_key, status)
- `app/Models/ProjectCredential` — Key/value secrets grouped by project name
- `app/Http/Controllers/Admin` — Blade CRUD for instances, credentials, users
- `app/Http/Controllers/Api` — Heartbeat + config export endpoints for backends
- `routes/web.php` — Blade routes (auth-protected dashboard, admin/)
- `routes/api.php` — `POST /api/v1/instances/heartbeat`, `GET /api/v1/instances/export`

### Databases
PostgreSQL creates two databases via `docker/init-databases.sql`:
- `admin_panel` — Laravel tables (instances, project_credentials, users)
- `autochess` — Backend-General tables (players, match_history)

### Nginx
`docker/nginx/laravel.conf` reverse-proxies the Admin Panel on host port 3001 (`nginx` service).

## Submodule Management
```bash
git submodule update --init --recursive   # after clone
git submodule update --remote --merge     # pull latest for all submodules
```

## Key Documentation
- `README.md` — project overview and submodule pointers
- `INSTALL.md` — full first-time setup (clone, env, migrate/seed, pairing)
- `PROGRESS.MD` — high-level phased progress tracker
- `AGENTS.md` — symlink to `AGENTS.md`
- Each submodule has its own `AGENTS.md` for local guidance

## Commit conventions

- Never add "model" or "cli" (or any AI/model/assistant name) to the git commit's `Co-Authored-By` trailer. Do not include a co-author trailer for AI tooling.
