# AutoChess Fullstack - Project Progress

Cross-component progress tracker. Per-backend detail lives in each
submodule's `PROGRESS.MD`.

---

## Phase 1: Core Infrastructure

| Area | Status |
|---|---|
| Docker orchestration (`docker-compose.yml`) | Done |
| PostgreSQL + Redis configuration (`docker/init-databases.sql`) | Done |
| `.env` + `pairing.json` pairing system | Done |
| CI/CD pipeline (GitHub Actions) | Done |

## Phase 2: Management & Security (Admin Panel)

| Area | Status |
|---|---|
| Laravel admin panel (fleet management) | Done |
| Push-based pairing from Admin Panel to backends | Done |
| Centralized secret management (project credentials, `inst_<id>` scoping) | Done |
| Heartbeat tracking of backend instances | Done |

## Phase 3: Backend Logic

Both backends are implemented in **Rust** (tokio · axum · tonic · sqlx).

### Backend-General (submodule)

| ID | Area | Status |
|---|---|---|
| BG-1..BG-2 | Player registration & login, JWT middleware | Done |
| BG-3..BG-4 | Redis matchmaker + delegation to Simulation | Done |
| BG-5 | gRPC `MatchNotification` server | Done |
| BG-6 | Match history persistence + admin query | Done |
| BG-7 | WebSocket hub (auth, queue, profile, history) | Done |
| BG-8 | Leaderboard | Done |
| BG-9 | Unit / integration tests | Done |
| BG-10..BG-12 | Real ELO, social system, cached global leaderboard | Pending |

### Backend-Simulation (submodule)

| ID | Area | Status |
|---|---|---|
| BS-1..BS-3 | Deterministic combat, abilities, status effects | Done |
| BS-4 | Match CRUD + Redis persistence + distributed lock | Done |
| BS-5..BS-6 | Shop + economy | Done |
| BS-7..BS-8 | Board movement + pairing | Done |
| BS-9 | Synergy evaluation (4/8 traits) | Partial |
| BS-10..BS-11 | Phase driver + outbound notifications | Pending |
| BS-12..BS-13 | Item equipping + full registry | Done |

### Cross-backend contracts

| Contract | Status |
|---|---|
| gRPC proto (`proto/match_service.proto`) | Done |
| HTTP match creation (`POST /api/match/create` from Gen to Sim) | Done |
| Pairing protocol (`POST /api/v1/pair` Admin to backends) | Done |
| Heartbeat protocol (`POST /api/v1/instances/heartbeat`) | Done |
| Config export (`GET /api/v1/instances/export`) | Done |

## Phase 4: Frontend & Client

| Area | Status |
|---|---|
| Submodule initialization (Game-Client v2, website placeholder) | Done |
| Game Client (Godot 4.7, WebSocket consumer, replay playback) | Partial |
| Game Website portal | Pending |

## CI/CD

| Job | Status |
|---|---|
| Backend-General (cargo test + build) | Working |
| Backend-Simulation (cargo test + build) | Working |
| Godot Linux export | Working |
| Godot Windows export | Working (requires fresh submodule fetch in CI cache) |
| Godot Android export | Working (requires godot-android image on GHCR) |
| Docker CI (godot-android image build + push to GHCR) | Working |

---

## Upcoming

1. **Backend-Simulation BS-9 (partial)** — define remaining 4 synergy traits.
2. **Backend-Simulation BS-10** — wire phase driver into production runtime.
3. **Backend-Simulation BS-11** — outbound gRPC + WS notifications to General.
4. **Backend-General BG-10** — real ELO (Glicko-2 or TrueSkill).
5. **Backend-General BG-11..BG-12** — social system + cached global leaderboard.
6. **Game Client GC-8..GC-12** — unit animations, HP/Mana bars, shop UI, lobby UI, result screen.
7. **Game Website** — public portal.
8. **End-to-end testing** — matchmaking to match creation to combat to result notification.

---

*Last Updated: 2026-08-28*
