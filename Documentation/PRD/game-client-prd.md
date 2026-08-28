now # Game-Client — Product Requirements Document (PRD)

> **Stack:** Godot 4.x (GDScript) — mobile-friendly canvas
> **Status:** Pending · **Date:** 2026-08-27
> **Parent PRD:** `Documentation/PRD/backend-general-prd.md`

---

## 1. Context

The visual client for AutoChess. Renders the 6x7 board grid and units, consumes
match results over WebSocket from Backend-General, and replays `BattleEvent` streams
deterministically client-side via a `ReplayDirector`. It does **not** simulate combat
locally — it plays back the exact action stream Backend-Simulation produced.

---

## 2. Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| GC-1 | WebSocket client connected to Backend-General `/ws` | Pending |
| GC-2 | Config loading from `project.godot` or config file | Pending |
| GC-3 | Deterministic replay (`ReplayDirector`) | Pending |
| GC-4 | 6x7 board grid rendering | Pending |
| GC-5 | Unit spawn, movement, attack, death animations | Pending |
| GC-6 | HP/Mana bars and floating damage numbers | Pending |
| GC-7 | Shop UI (roll, buy, sell) | Pending |
| GC-8 | Full match flow UI (lobby, draft, battle, result) | Pending |

---

## 3. WebSocket Protocol

### Client Actions (sent to Backend-General WS)

| Action | Payload |
|--------|---------|
| `login` | `{username, password}` |
| `register` | `{username, password, display_name?}` |
| `queue_join` | — |
| `queue_leave` | — |
| `get_profile` | — |
| `get_history` | — |

### Server Events (received)

| Event | Source | Description |
|-------|--------|-------------|
| `auth_success` | General | Login/register success, contains JWT token |
| `auth_error` | General | Authentication failure |
| `queue_update` | General | Current queue size |
| `match_found` | General | Match ready, contains match_id + server_url |
| `profile` | General | Player profile data |
| `history` | General | Match history list |
| `eliminated` / `victory` | General | Match result after Simulation notifies via gRPC |

---

## 4. Verification

```bash
# Start backends
cd Backend/Backend-General && cargo run
cd Backend/Backend-Simulation && cargo run

# Open Game-Client in Godot Editor
# Connect to ws://localhost:8081/ws
# Register/login, queue, verify match_found + replay playback
```
