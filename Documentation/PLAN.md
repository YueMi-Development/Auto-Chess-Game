# AutoChess Fullstack — Product Requirements Document (PRD)

> **Type:** PRD · **Scope:** Main monorepo (orchestration + cross-component contracts)
> **Date:** 2026-08-19 · **Status:** Reflects verified implementation state (not just docs)

---

## 1. Context

AutoChess Fullstack is a modular auto-battler inspired by *Teamfight Tactics* and *Magic Chess*.
Players draft units, manage economy, and watch their team battle automatically on a 6×7 grid.
The product is a **Git submodule monorepo** spanning five independently-versioned components:

| Component | Stack | Role | Status |
|-----------|-------|------|--------|
| Admin-Area/Admin-Panel | Laravel 12 (PHP 8.2) | Fleet management, secrets, pairing | ~95% |
| Backend/Backend-General | Rust (tokio/axum/tonic) | Players, auth, matchmaking, WS hub, gRPC server | ~85% |
| Backend/Backend-Simulation | Rust (tokio/axum) | Match engine, deterministic combat, shop, synergies | ~90% |
| Frontend/Game-Client | Godot 4.x (GDScript) | Visual playback engine, WebSocket consumer | Pending |
| Frontend/Game-Website | (undecided) | Landing page + player portal | ~10% |

> Each submodule also has its own `PLAN.md` with its full requirement breakdown. This file
> covers the **shared contracts and orchestration** that tie them together.

---

## 2. System Architecture

```mermaid
flowchart TD
    subgraph Clients
        GC["Game-Client\n(Unity C# / URP)"]
        GW["Game-Website\n(placeholder)"]
    end

    subgraph Core["Backend (Rust)"]
        BG["Backend-General\nplayers · auth · matchmaking\nWS hub · gRPC server\ntokio · axum · tonic"]
        BS["Backend-Simulation\nmatch engine · deterministic combat\nshop · synergies\ntokio · axum"]
    end

    subgraph Ops
        AP["Admin-Panel\n(Laravel 12)"]
    end

    subgraph Data
        PG[("PostgreSQL\nadmin_panel + autochess")]
        RD[("Redis\nqueue · pub/sub · lock")]
    end

    GC -- "WebSocket /ws" --> BG
    GW -. "HTTP (planned)" .-> BG
    BG -- "REST /api/match/create" --> BS
    BS -- "gRPC MatchNotification :50051" --> BG
    AP -- "pairing + heartbeat + export" --> BG
    AP -- "pairing + heartbeat + export" --> BS
    BG --> PG
    BG --> RD
    BS --> RD
    AP --> PG
```

### Build targets

- **Backend-General** — `cargo build --release` → Linux x86_64 binary (primary); Docker (Windows)
- **Backend-Simulation** — `cargo build --release` → Linux x86_64 binary (primary); Docker (Windows)

### Service ports (docker-compose)

| Service | Port(s) | Notes |
|---------|---------|-------|
| Admin Panel (nginx) | 3001 | Laravel interface |
| Backend-General | 8081 (HTTP) / 50051 (gRPC) | REST + WS + gRPC server |
| Backend-Simulation | 8082 | Match/combat engine |
| PostgreSQL | 5432 | `admin_panel` + `autochess` databases |
| Redis | 6379 | Matchmaking queue / caching |

---

## 3. Cross-Cutting Requirements

### 3.1 Push-based pairing & config resolution

All server-side components share a **push-based pairing** lifecycle — the single most
important cross-component contract.

```mermaid
sequenceDiagram
    participant Op as Operator
    participant AP as Admin-Panel
    participant BE as Rust backend
    participant DB as PostgreSQL

    Op->>AP: Create Instance (name, type, endpoint)
    AP->>AP: pairing_key = "inst_" + random(32)
    AP->>BE: POST {endpoint}/api/v1/pair {admin_url, pairing_key}
    BE-->>AP: 200 OK
    AP->>DB: store Instance (status=online)

    loop every 30s
        BE->>AP: POST /api/v1/instances/heartbeat {instance_key, ip, port, key_count, effective_hash}
        AP->>DB: update last_heartbeat_at / status=online
    end

    BE->>AP: GET /api/v1/instances/export?instance_key=X&scopes=Shared
    AP-->>BE: .env-formatted text (text/plain)<br/>scopes: Shared → inst_<id>

    Op->>AP: Unpair / Delete
    AP->>BE: POST {endpoint}/api/v1/unpair {pairing_key}
    BE-->>AP: 200 OK (deletes pairing.json)
```

**Config resolution order (Rust backends, later overrides earlier):**

```mermaid
flowchart TD
    A["1. OS Env / .env (godotenv)"] --> B["2. pairing.json (admin_url + instance_key)"]
    B --> C["3. Remote Admin-Panel export (Shared → inst_<id>)"]
    C --> D["Final effective config"]
```

### 3.2 Determinism guarantee (replay)

Combat is **deterministic**: identical seed + input ⇒ identical `BattleResult` event stream.
This lets the Unity client replay a match locally without re-simulating.

```mermaid
flowchart LR
    SEED["Seed (int64)"] --> RNG["DeterministicRNG<br/>(math/rand)"]
    RNG --> SIM["BattleEngine<br/>tick-by-tick"]
    SIM --> EV["BattleEvent stream<br/>(move/attack/death/ability)"]
    EV --> CLIENT["Unity ReplayDirector<br/>local playback @ ~100 TPS"]
```

- Units processed in **sorted-ID order**; BFS movement order fixed (up/down/left/right);
  nearest-enemy tie-break by (row, col).
- Match-level seed = `match.Seed + round` (+ gold for rerolls).

### 3.3 Cross-component data contracts

```mermaid
flowchart TD
    subgraph "MatchNotification (gRPC, BS → BG)"
        PE["PlayerEliminated(match_id, player_id, placement)"]
        PW["PlayerWon(match_id, player_id)"]
        MF["MatchFinished(match_id, placements[], rounds_played)"]
    end

    subgraph "Match create (HTTP, BG → BS)"
        MC["POST /api/match/create<br/>{player_ids, seed, max_players} → {match_id}"]
    end

    subgraph "WebSocket events (BG → Client)"
        E1["auth_success / auth_error"]
        E2["queue_update / match_found"]
        E3["profile / history"]
        E4["eliminated / victory / error"]
    end
```

### 3.4 Fleet & credentials resolution

The system runs **N General instances and M Simulation instances**
simultaneously (multi-region, A/B, canary). Credentials are scoped
per-instance, never per-type. Each instance gets its own `inst_<id>`
scope; backend type is metadata only.

```mermaid
flowchart LR
    subgraph DB["Admin-Panel Postgres"]
      T1[("Shared rows\nShared")]
      T2[("General-A rows\ninst_aaa")]
      T3[("General-B rows\ninst_bbb")]
      T4[("Simulation-C rows\ninst_ccc")]
    end

    X(["GET /api/v1/instances/export\n?instance_key=A&scopes=Shared"]) --> Y["text/plain .env body\nmerge: Shared → inst_aaa"]
    X2(["GET /api/v1/instances/export\n?instance_key=B&scopes=Shared"]) --> Y2["text/plain .env body\nmerge: Shared → inst_bbb"]
    X3(["GET /api/v1/instances/export\n?instance_key=C&scopes=Shared"]) --> Y3["text/plain .env body\nmerge: Shared → inst_ccc"]

    T1 --> X
    T2 --> X
    T1 --> X2
    T3 --> X2
    T1 --> X3
    T4 --> X3

    Y --> A["General-A\n(Rust)\ninst_aaa"]
    Y2 --> B["General-B\n(Rust)\ninst_bbb"]
    Y3 --> C["Simulation-C\n(Rust)\ninst_ccc"]
```

> **Merge order:** `Shared` → `inst_<id>`. Last write wins. One instance
> never sees another's per-scope keys. The Admin Panel always appends
> `inst_<id>` server-side regardless of what the URL query requested.

```mermaid
sequenceDiagram
    participant BE as Rust backend
    participant AP as Admin-Panel
    participant DB as PostgreSQL

    BE->>AP: POST /api/v1/pair {admin_url, pairing_key}
    AP->>DB: lookup Instance by pairing_key
    DB-->>AP: instance.id = "inst_aaa"
    AP-->>BE: 200 OK (writes pairing.json)

    BE->>AP: GET /api/v1/instances/export?instance_key=…&scopes=Shared
    AP->>DB: SELECT * FROM project_credentials<br/>WHERE project_name IN ('Shared','inst_aaa')
    DB-->>AP: rows
    AP-->>BE: 200 text/plain<br/>Shared rows first → inst_aaa rows last

    loop every 30s
        BE->>AP: POST /heartbeat {…, key_count, effective_hash}
        AP->>DB: persist hash + key_count
    end
```

Drift detection: heartbeat carries `effective_hash`
(SHA-256 of sorted `KEY=VALUE` pairs) and `key_count`. The Admin UI
flags mismatches and offers a "Re-push credentials" action. See
`CREDENTIALS.md` for the full spec.

---

## 4. End-to-End Match Flow (target state)

The primary user journey the product must deliver.

```mermaid
sequenceDiagram
    participant P as Player
    participant C as Game-Client
    participant G as Backend-General
    participant S as Backend-Simulation

    P->>C: open game
    C->>G: WebSocket connect /ws
    P->>C: register / login
    C->>G: {action: login}
    G-->>C: auth_success {token, player}

    P->>C: queue_join
    C->>G: {action: queue_join}
    G-->>C: queue_update

    Note over G: 8 players queued
    G->>S: POST /api/match/create
    S-->>G: {match_id}
    G-->>C: match_found {match_id, server_url}

    C->>S: WebSocket /ws/match
    loop round loop (shop → battle → damage)
        S->>S: StartRound → RunBattlePhase → ApplyDamage
        S-->>C: state_update / battle_result
    end

    S->>G: gRPC PlayerEliminated / MatchFinished
    G-->>C: eliminated / victory (pub/sub fan-out)
    C->>C: ReplayDirector plays final BattleResult
```

> ⚠️ The round loop (`StartRound` → `RunBattlePhase` → `ApplyDamage`) and outbound result
> notifications are **not yet wired** in production — see the gap register below.

---

## 5. Consolidated Gap Register

Priority-ordered gaps that block the full product experience. Full details live in each
submodule's `PLAN.md`.

```mermaid
flowchart TD
    subgraph Blockers["Blockers (core loop incomplete)"]
        B1["Simulation: no round/phase driver exposed"]
        B2["Simulation: no outbound result notifications"]
        B3["Simulation: EquipItem stub"]
        B4["Client: message routing only handles BattleResult"]
    end
    subgraph Major["Major (correctness/robustness)"]
        M1["Simulation: synergy double-count bug fixed ✓"]
        M2["Simulation: incomplete synergy registry (4/8)"]
        M3["Simulation: deterministic combat 36 tests ✓"]
        M4["General: no integration tests"]
        M5["Client: no HP tracking in replay"]
    end
    subgraph Minor["Minor (hardening/polish)"]
        N1["Admin: is_secret not enforced"]
        N2["Admin: endpoint not editable"]
        N3["General: WS origin validation"]
        N4["General: health check ✓ (done)"]
        N5["Admin: no offline detection"]
    end
```

| # | Component | Gap | Impact | Status |
|---|-----------|-----|--------|--------|
| 1 | Simulation | No phase-advance driver | Match never progresses in production | Pending |
| 2 | Simulation | No outbound notifications | General never learns results | Pending |
| 3 | Simulation | `EquipItem` stub | Items can't be equipped | Pending |
| 4 | Client | Heuristic message routing | Client ignores auth/queue/match_found | Pending |
| 5 | Simulation | Deterministic combat | Core engine | ✅ Done (42 tests) |
| 6 | Simulation | Synergy double-count | Incorrect trait thresholds | ✅ Fixed (dedup by hero-id) |
| 7 | Simulation | Incomplete synergy registry | Most traits do nothing | Pending (4/8) |
| 8 | General | No integration tests | Regression risk | Pending |
| 9 | General | Double-record risk | Rating/stats double-applied | ✅ Fixed (idempotency + unique constraint) |
| 10 | Admin | `is_secret` not enforced | Secrets leak as plaintext | Pending |
| 11 | Admin | No offline detection | Stale "online" status | Pending |
| 12 | All | Per-fleet credential scoping | Many instances of one type share secrets | ✅ Done (inst_\<id\>) |

---

## 6. Delivery Roadmap (recommended phasing)

```mermaid
gantt
    title AutoChess Delivery Roadmap
    dateFormat  YYYY-MM-DD
    section Backend
    Wire round-loop driver + notifications :r1, 2026-09-01, 20d
    Fix synergy registry + double-count    :r2, 2026-09-15, 15d
    Item equipping                          :r3, 2026-10-01, 15d
    General tests + idempotency             :r4, 2026-10-01, 15d
    section Client
    Typed message envelope + full flow UI   :c1, 2026-09-20, 30d
    HP tracking + shop UI                   :c2, 2026-10-15, 20d
    section Ops
    is_secret enforcement + offline detect  :o1, 2026-09-15, 15d
    section Website
    Framework selection + landing page      :w1, 2026-10-01, 30d
```

---

## 7. Verification (end-to-end)

```bash
# 1. Full-stack smoke
cp .env.example .env && docker compose up -d --build
docker compose exec admin-panel php artisan migrate --force
docker compose exec admin-panel php artisan db:seed --class=InitialSetupSeeder --force

# 2. Backend-Simulation (Rust) — 42 tests, determinism, synergy
cd Backend/Backend-Simulation && cargo test && cargo build --release

# 3. Backend-General (Rust) — 4 tests, auth, rating table
cd Backend/Backend-General && cargo test && cargo build --release

# 4. Admin Panel
docker compose exec admin-panel php artisan test

# 5. Health + flow
curl http://localhost:8081/healthz
```

Then: pair instances in Admin Panel → register 8 players → queue → verify `match_found` →
create match → verify round loop emits `battle_result` + gRPC callbacks (once gaps 1–2 are fixed).

---

*End of PRD. Update §5–§6 as gaps close.*
