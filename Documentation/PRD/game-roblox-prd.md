# Game-Roblox — Product Requirements Document (PRD)

> **Stack:** Roblox Studio + Lua, Rojo build system
> **Status:** Pending · **Date:** 2026-08-31
> **Parent PRD:** `Documentation/PRD/backend-general-prd.md`

---

## 1. Context

The Roblox-based game client for AutoChess. Built on Roblox Studio with Lua scripts managed by [Rojo](https://rojo.space/). Unlike the Godot client, Roblox does not support WebSocket connections — all communication with `Backend-General` is over HTTP REST via `HttpService`. The client polls for game state updates.

---

## 2. Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| GR-1 | HTTP client via `HttpService` connected to `Backend-General` | Pending |
| GR-2 | Config loading from a remote config endpoint or hardcoded defaults | Pending |
| GR-3 | Player authentication (register / login via REST) | Pending |
| GR-4 | Matchmaking via REST polling (`/api/matchmaking/status`) | Pending |
| GR-5 | Game state polling and board rendering (6x7 grid) | Pending |
| GR-6 | Unit spawn, movement, attack, death animations | Pending |
| GR-7 | HP/Mana bars and floating damage numbers | Pending |
| GR-8 | Shop UI (roll, buy, sell via REST) | Pending |
| GR-9 | Full match flow UI (lobby, draft, battle, result) | Pending |
| GR-10 | Rojo project scaffold (`default.project.json`, `src/`) | Pending |

---

## 3. REST Protocol

Roblox `HttpService` only supports HTTP — no WebSocket.

### Client Actions (POST / GET to Backend-General)

| Action | Method | Endpoint | Payload |
|--------|--------|----------|---------|
| Register | POST | `/api/auth/register` | `{username, password, display_name?}` |
| Login | POST | `/api/auth/login` | `{username, password}` |
| Join queue | POST | `/api/matchmaking/join` | — |
| Leave queue | POST | `/api/matchmaking/leave` | — |
| Get queue status | GET | `/api/matchmaking/status` | — |
| Get game state | GET | `/api/game/state` | — |
| Send action | POST | `/api/game/action` | `{action_type, payload}` |
| Get profile | GET | `/api/profile` | — |
| Get match history | GET | `/api/history` | — |

### Server Responses

| Response | Description |
|----------|-------------|
| `{success, token}` | Auth success, contains JWT |
| `{success, match_id, server_url}` | Match found |
| `{state: {...}}` | Full game state snapshot |
| `{events: [...]}` | Event log since last poll |

---

## 4. Architecture

```
Frontend/Game-Roblox/
├── default.project.json   # Rojo project config
└── src/
    ├── Server/           # Server scripts (run on Roblox server)
    │   └── Server.lua    # Bridges Roblox server events ↔ REST API
    ├── Shared/           # Shared scripts (replicated to all clients)
    │   └── Shared.lua    # Game constants, data models, utilities
    └── Client/          # Client scripts (run per-player)
        └── Client.lua    # UI, board rendering, user input
```

### Communication Flow

```
Roblox Client (HttpService)
  └── HTTP REST ──► Backend-General (port 8081)
                        │ gRPC
                        ▼
                  Backend-Simulation (port 8082)
                        │ HTTP heartbeat
                        ▼
                  Admin-Panel (port 3001)
```

---

## 5. Polling Strategy

Since Roblox has no WebSocket, the client uses timed polling:

| Poll | Interval | Purpose |
|------|----------|---------|
| Game state | 1–2s | Near-realtime board updates |
| Matchmaking | 2–3s | Queue status |
| Profile/History | On demand | User data |

> **Note:** If latency becomes a problem, consider using `MessagingService` for internal Roblox pub/sub between server and client scripts, with the server script as the sole HTTP caller.

---

## 6. Verification

```bash
# Start backends
cd Backend/Backend-General && cargo run
cd Backend/Backend-Simulation && cargo run

# Serve Roblox project
cd Frontend/Game-Roblox && rojo serve

# Open Rojo plugin in Roblox Studio, connect to the server
# Register/login, join queue, verify polling and game state rendering
```
