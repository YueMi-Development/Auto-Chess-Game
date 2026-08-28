# 🏆 AutoChess Fullstack - Project Progress

Cross-component progress tracker. Per-backend detail lives in each
submodule's `PROGRESS.MD`.

---

## 🚦 Phase 1: Core Infrastructure

| Area | Status |
|---|---|
| Docker orchestration (`docker-compose.yml`) | ✅ |
| PostgreSQL + Redis configuration (`docker/init-databases.sql`) | ✅ |
| `.env` + `pairing.json` pairing system | ✅ |
| CI/CD pipeline | ❌ Pending |

## 🛠️ Phase 2: Management & Security (Admin Panel)

| Area | Status |
|---|---|
| Laravel admin panel (fleet management) | ✅ |
| Push-based pairing from Admin Panel to backends | ✅ |
| Centralized secret management (project credentials, `inst_<id>` scoping) | ✅ |
| Heartbeat tracking of backend instances | ✅ |

## ⚔️ Phase 3: Backend Logic

Both backends are implemented in **Rust** (tokio · axum · tonic · sqlx).

### Backend-General (submodule pointer)

| ID | Area | Status |
|---|---|---|
| BG-1..BG-2 | Player registration & login, JWT middleware | ✅ |
| BG-3..BG-4 | Redis matchmaker + delegation to Simulation | ✅ |
| BG-5 | gRPC `MatchNotification` server | ✅ |
| BG-6 | Match history persistence + admin query | ✅ |
| BG-7 | WebSocket hub (auth, queue, profile, history) | ✅ |
| BG-8 | Leaderboard | ✅ |
| BG-9 | Unit / integration tests | ✅ |
| BG-10..BG-12 | Real ELO, social system, cached global leaderboard | ❌ Pending |

### Backend-Simulation (submodule pointer)

| ID | Area | Status |
|---|---|---|
| BS-1..BS-3 | Deterministic combat, abilities, status effects | ✅ |
| BS-4 | Match CRUD + Redis persistence + distributed lock | ✅ |
| BS-5..BS-6 | Shop + economy | ✅ |
| BS-7..BS-8 | Board movement + pairing | ✅ |
| BS-9 | Synergy evaluation (4/8 traits) | ⚠️ Partial |
| BS-10..BS-11 | Phase driver + outbound notifications | ❌ Pending |
| BS-12..BS-13 | Item equipping + full registry | ✅ |

### Cross-backend contracts

| Contract | Status |
|---|---|
| gRPC proto (`proto/match_service.proto`) | ✅ |
| HTTP match creation (`POST /api/match/create` from Gen → Sim) | ✅ |
| Pairing protocol (`POST /api/v1/pair` Admin → backends) | ✅ |
| Heartbeat protocol (`POST /api/v1/instances/heartbeat`) | ✅ |
| Config export (`GET /api/v1/instances/export`) | ✅ |

### Build verification

```bash
# Backend-Simulation — 42 tests
cd Backend/Backend-Simulation && cargo test && cargo build --release

# Backend-General — 4 tests
cd Backend/Backend-General && cargo test && cargo build --release
```

## Phase 4: Frontend & Client

| Area | Status |
|---|---|
| Submodule initialization (Game-Client v2, website placeholder) | ✅ |
| Game Website portal | ❌ Pending |
| Game Client (Godot 4, WebSocket consumer, replay playback) | ❌ Pending |

---

## 📅 Upcoming

1. **Backend-Simulation BS-9 (partial)** — define remaining 4 synergy traits.
2. **Backend-Simulation BS-10** — wire phase driver into production runtime.
3. **Backend-Simulation BS-11** — outbound gRPC + WS notifications to General.
4. **Backend-General BG-10** — real ELO (Glicko-2 or TrueSkill).
5. **Backend-General BG-11..BG-12** — social system + cached global leaderboard.
6. **CI/CD pipeline** — Dockerfile-based build pipeline for Rust backends.
7. **Frontend kickoff** — Game Client (Unity URP) consumes WebSocket once BS-11 lands.
8. **End-to-end testing** — matchmaking → match creation → combat → result
   notification → history once BS-10/BS-11 are complete.

---

*Last Updated: 2026-08-27*
