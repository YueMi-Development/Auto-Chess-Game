# Backend-Simulation — Product Requirements Document (PRD)

> **Stack:** Rust (tokio/axum)
> **Status:** ~75% complete · **Date:** 2026-08-19
> **Parent PRD:** `Documentation/PRD/backend-general-prd.md`

---

## 1. Context

The match engine for AutoChess: deterministic tick-by-tick combat, match lifecycle, round
management, shop/economy, board movement, and synergy/trait evaluation. Uses Redis as the source
of truth; results are broadcast to clients via WebSocket and notified to Backend-General via gRPC.

---

## 2. Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| BS-1 | Deterministic tick combat (crit/dodge/lifesteal/mana) | Done |
| BS-2 | 5 ability types (`single_target`, `area_damage`, `heal`, `buff`, `multi_arrow`) | Done |
| BS-3 | 5 status effects (`stun`, `silence`, `burn`, `freeze`, `hot`) | Done |
| BS-4 | Match CRUD with Redis persistence + distributed lock | Done |
| BS-5 | Shop (roll/reroll/buy/sell/star-upgrade) | Done |
| BS-6 | Economy (income/interest/streak/XP) | Done |
| BS-7 | Board/bench movement (6x7 grid) | Done |
| BS-8 | Pairing (shuffle + ghost clone) | Done |
| BS-9 | Synergy evaluation + stat buffs | Partial |
| BS-10 | Round/phase driver exposed over HTTP/WS | Pending |
| BS-11 | Outbound result notifications fired | Pending |
| BS-12 | Item equipping | Pending |
| BS-13 | Hero/item/skill/synergy registry | Partial |

---

## 3. Match Lifecycle

```
created ---> shop ---> battle ---> damage ---> [next round or finished]
```

---

## 4. API Surface

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/simulate` | One-off battle simulation |
| POST | `/api/sample` | Sample `BattleConfig` |
| GET | `/api/heroes` | List heroes |
| GET | `/api/skills` | List skills |
| GET | `/api/items` | List items |
| GET | `/api/synergies` | List synergies |
| POST | `/api/match/create` | Create match |
| GET | `/api/match/state?match_id=` | Current match state |
| GET | `/ws/match?match_id=&player_id=` | WebSocket upgrade |
| POST | `/api/v1/pair` · `/unpair` | Admin Panel pairing |

---

## 5. Verification

```bash
cd Backend/Backend-Simulation && cargo test && cargo build --release
```
