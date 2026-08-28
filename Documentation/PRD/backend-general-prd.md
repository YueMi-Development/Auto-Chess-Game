# Backend-General — Product Requirements Document (PRD)

> **Stack:** Rust (tokio/axum/tonic)
> **Status:** ~80% complete · **Date:** 2026-08-19
> **Parent PRD:** `Documentation/PRD/backend-general-prd.md`

---

## 1. Context

The persistent core of the AutoChess system: players, authentication, matchmaking orchestration,
match history, and real-time WebSocket communication. Boots three servers simultaneously —
HTTP REST, gRPC, and a WebSocket hub.

It delegates match simulation to Backend-Simulation over HTTP and receives results back via gRPC.

---

## 2. Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| BG-1 | Player registration/login (bcrypt + JWT HS256) | Done |
| BG-2 | JWT-protected REST (Bearer — `X-Player-ID`) | Done |
| BG-3 | Redis matchmaker (8-player batch, distributed lock) | Done |
| BG-4 | Match creation delegation (`POST /api/match/create`) | Done |
| BG-5 | gRPC `MatchNotification` server (3 RPCs) | Done |
| BG-6 | Match history persistence + query | Done |
| BG-7 | WebSocket hub (auth, queue, profile, history, pub/sub) | Done |
| BG-8 | Leaderboard (`ORDER BY rating DESC`) | Done |
| BG-9 | Unit / integration tests | Pending |
| BG-10 | Real ELO / ranked season logic | Planned |
| BG-11 | Friendship / social system | Planned |
| BG-12 | Global leaderboard aggregation (cached) | Planned |

---

## 3. REST Endpoints

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| POST | `/api/auth/register` | public | Create player |
| POST | `/api/auth/login` | public | Returns `{token, player}` |
| POST | `/api/v1/pair` | pairing | Admin Panel pairing |
| POST | `/api/v1/unpair` | pairing_key | Depair |
| GET | `/api/admin/leaderboard` | public | Top players |
| GET | `/api/admin/players` | JWT | List players |
| GET | `/api/admin/matches` | JWT | List matches |
| GET | `/ws` | socket | WebSocket upgrade |

---

## 4. WebSocket Protocol

### Client Actions (type=action)

`login`, `register`, `queue_join`, `queue_leave`, `get_profile`, `get_history`

### Server Events (type=event)

`auth_success`, `auth_error`, `queue_update`, `match_found`, `profile`, `history`,
`eliminated`, `victory`, `error`

---

## 5. Verification

```bash
cd Backend/Backend-General && cargo test && cargo build --release
```
