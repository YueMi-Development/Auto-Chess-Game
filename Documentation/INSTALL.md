# Installation Guide

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- Git (with submodule support)

## 1. Clone the Repository

```bash
git clone --recurse-submodules https://github.com/YueMi-Development/Auto-Chess-Game.git
cd AutoChess-Fullstack
```

If you already cloned without submodules:

```bash
git submodule update --init --recursive
```

## 2. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and configure at minimum:

| Variable | Description |
|----------|-------------|
| `POSTGRES_PASSWORD` | Strong password for databases |
| `APP_KEY` | Laravel App Key (Run `php artisan key:generate` to create) |
| `GENERAL_JWT_SECRET` | Secret for Backend General authentication |

## 3. Start All Services

```bash
docker compose up -d --build
```

Wait for all containers to become healthy.

## 4. Initialize Admin Panel

You must run migrations and seeders once for the Laravel Admin Panel:

```bash
docker compose exec admin-panel php artisan migrate --force
docker compose exec admin-panel php artisan db:seed --class=InitialSetupSeeder --force
```

### Accessing the Panel

Open [http://localhost:3001](http://localhost:3001) and log in with the credentials
set by the seeder. Change the default password immediately after first login.

## 5. Admin-Initiated Pairing

The system uses a **Push-based Pairing** model. You do not need to manually copy keys
into backend `.env` files anymore.

### Pairing Steps

1. Log in to the **Admin Panel**.
2. Navigate to **Instances** -> **Add Instance**.
3. Enter a **Name**, **Type** (`general` or `simulation`), and the **Instance Endpoint**.
4. Click **Create & Pair**.
5. The Admin Panel will push the credentials to the backend. The backend will save them
   to a local `pairing.json` and report as **Online**.

## 6. Service Infrastructure

| Service | Port | Description |
|---------|------|-------------|
| Admin Panel | 3001 | Laravel Interface (Auth, Fleet, Secrets) |
| Backend General | 8081 | Core Game Logic & API |
| Backend Simulation | 8082 | Match & Combat Simulation |
| PostgreSQL | 5432 | Primary Data Store |
| Redis | 6379 | Pub/Sub & Caching |

## 7. Configuration Exports

Backends fetch their secrets (DB URLs, third-party keys) from the Admin Panel.
- **Auto-Loading**: On startup, backends contact the Admin Panel using their stored `pairing_key`.
- **Scopes**: Use `CREDS_MANAGER_SCOPES=Shared,general` in your backend environment to
  control which secret groups are fetched.

## 8. Configuration Overrides

When a backend starts, configuration is resolved in this order (later overrides earlier):

1. **Environment Variables** (`.env` or OS) — Baseline fallback.
2. **Local Persistence** (`pairing.json`) — Overrides Admin URL and Instance Key.
3. **Remote Config (Laravel)** — Overrides everything else with the latest secrets from the database.

## 9. Running Standalone (For Developers)

### Backend General

```bash
cd Backend/Backend-General
cargo run
```

### Backend Simulation

```bash
cd Backend/Backend-Simulation
cargo run
```

*Note: Standalone backends will try to find `pairing.json`. If missing, they will wait
for a pairing push on their HTTP port.*

## 10. Verify

Check that all services are running:

```bash
docker compose ps
docker compose logs -f
```

Test health endpoints:

```bash
curl http://localhost:3001/api/health
curl http://localhost:8081/api/health
```

## Stopping

```bash
docker compose down
```

To also remove stored data (databases, Redis):

```bash
docker compose down -v
```

## Troubleshooting

- **Admin Key Missing**: Run `docker compose exec admin-panel php artisan key:generate`
  to fix 500 errors on the panel.
- **Instance Offline**: Check the `pairing_key` matches between `pairing.json` and the Admin UI.
- **Connection Refused**: Ensure `admin-panel` is reachable from the backend using the
  Docker service name.
