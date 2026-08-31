# Backend-MatchGames — Match Lifecycle — Product Requirements Document (PRD)

> **Stack:** Rust (tokio/axum)
> **Status:** ~80% complete · **Date:** 2026-08-31**
> **Architecture:** 4-service split (General → Matchmaking → MatchGames → Simulation)

---

## 1. Context

Match lifecycle orchestration service. Receives match creation requests from Backend-Matchmaking,
manages in-memory match state, runs round loops (shop → battle → round-end), delegates battle
simulation to Backend-Simulation, and writes results to the database.

Receives players as **external IDs** (from Matchmaking) and resolves them to internal player IDs
via DB lookup.

---

## 2. Service Topology

```mermaid
flowchart LR
    BM[":8083 Matchmaking"]
    BMG[":8084 MatchGames"]
    BS[":8082 Simulation"]
    BG[":8081 General"]
    DB["(:5432 PostgreSQL<br/>admin_panel)"]

    BM -->|"POST /match/create<br/>{match_id, player_ids[]}"| BMG
    BMG <-->|"resolve external_id|write matches/history"| DB
    BMG -->|"POST /simulate"| BS
    BS -->|"won_by, lost_by,<br/>damage_dealt[]"| BMG
    BMG -.->|"gRPC MatchNotification"| BG
```

---

## 3. Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| MG-1 | `POST /api/match/create` (resolve external IDs, write to DB) | Done |
| MG-2 | In-memory `MatchState` registry (DashMap) | Done |
| MG-3 | Round loop: shop_phase → battle_phase → round_end | Done |
| MG-4 | Call Backend-Simulation for battle resolution | Done |
| MG-5 | Apply battle damage (loser: `2 + round/3` HP) | Done |
| MG-6 | Eliminate players at 0 HP | Done |
| MG-7 | Write `match_history` entries after each battle | Done |
| MG-8 | Update `matches.status` to completed/terminated | Done |
| MG-9 | WebSocket `/ws/match/:id` for live match events | Partial |
| MG-10 | gRPC pairing with Admin Panel (ULID instance_id + RegisterInstance + heartbeat) | Done |
| MG-11 | gRPC client to notify Backend-General on match end | Planned |

---

## 4. Match Phase Flow

```mermaid
stateDiagram-v2
    [*] --> STARTING
    STARTING --> SHOP_PHASE: 8 players ready
    SHOP_PHASE --> BATTLE_PHASE: 30s timer
    BATTLE_PHASE --> ROUND_END: combat resolved
    ROUND_END --> SHOP_PHASE: 5s timer
    ROUND_END --> FINISHED: 1 player left
    ROUND_END --> FINISHED: round 30 reached
    BATTLE_PHASE --> TERMINATED: error
    SHOP_PHASE --> TERMINATED: error
    FINISHED --> [*]
    TERMINATED --> [*]
```

**Phase durations:**
- Shop Phase: 30 seconds
- Round End: 5 seconds
- Battle Phase: variable (determined by combat)

---

## 5. API Endpoints

| Method | Path | Body / Params | Response |
|--------|------|---------------|----------|
| POST | `/api/match/create` | `{"match_id": "ULID", "player_ids": ["RBLX...","RBLX..."]}` | `{"success": true, "match_id": "ULID"}` |
| GET | `/api/match/:id/state` | — | `MatchState` JSON |
| WS | `/ws/match/:id` | — | Live match events stream |
| GET | `/health` | — | `"ok"` |

### `GET /api/match/:id/state` Response

```json
{
  "match_id": "01ARZ3NYREPGMT7RRFF6699PS",
  "players": [
    {
      "player_id": 1,
      "external_id": "RBLX12345_Sfx",
      "gold": 50,
      "health": 100,
      "board": [],
      "bench": [],
      "level": 1
    }
  ],
  "phase": "shop_phase",
  "round": 3,
  "started_at": "2026-08-31T00:00:00Z",
  "updated_at": "2026-08-31T00:01:30Z"
}
```

---

## 6. Battle Resolution

```mermaid
sequenceDiagram
    participant BMG as MatchGames
    participant BS as Simulation
    participant DB as PostgreSQL

    Note over BMG: Battle Phase begins
    BMG->>BS: POST /api/simulate {players, board}
    BS-->>BMG: {won_by: 0, lost_by: 1, damage_dealt: [...]}
    Note over BMG: Apply damage:<br/>loser.health -= 2 + (round/3)
    BMG->>DB: INSERT match_history (placement, is_winner)
    alt player.health <= 0
        Note over BMG: Remove from alive_players
    end
    alt alive_players.length <= 1
        Note over BMG: Transition to FINISHED
    else
        Note over BMG: Transition to ROUND_END
    end
```

---

## 7. Database Schema (admin_panel)

```mermaid
erDiagram
    MATCHES {
        bigint id PK
        string ulid UK
        string status "starting|running|completed|canceled|terminated"
        int player_count
        timestamp created_at
        timestamp updated_at
    }
    MATCH_HISTORY {
        bigint id PK
        bigint match_id FK
        bigint player_id FK
        int placement
        bool is_winner
        timestamp created_at
    }
    PLAYERS {
        bigint id PK
        string external_id UK
        string source "WEB|GAME|ROBLOX"
    }

    MATCHES ||--o{ MATCH_HISTORY : ""
    PLAYERS ||--o{ MATCH_HISTORY : ""
```

---

## 8. Config

| Env Var | Default | Description |
|---------|---------|-------------|
| `DATABASE_URL` | `postgres://.../admin_panel` | PostgreSQL connection |
| `BACKEND_SIMULATION_URL` | `http://backend-simulation:8082` | Simulation base URL |
| `BACKEND_GENERAL_URL` | `http://backend-general:8081` | General lobby base URL |
| `ADMIN_GRPC_ADDR` | `localhost:50052` | Backend-AdminGrpc gRPC address |

Config resolution: env → `pairing.json` → Admin Panel remote export.

---

## 9. Verification

```bash
cd Backend/Backend-MatchGames && cargo test && cargo build --release
```
