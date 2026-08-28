# Game-Website — Product Requirements Document (PRD)

> **Stack:** Undecided (React / Next.js being evaluated)
> **Status:** ~10% (placeholder) · **Date:** 2026-08-19
> **Parent PRD:** `Documentation/PRD/backend-general-prd.md`

---

## 1. Context

The planned landing page and player portal for AutoChess: account management, profile viewing,
match history, and a global leaderboard.

This is a placeholder submodule — no application code, framework, or build tooling exists yet.

---

## 2. Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| GW-1 | Select framework (React/Next.js) | Evaluating |
| GW-2 | User portal (profile viewing, match history) | Planned |
| GW-3 | Global leaderboard (real-time ranking) | Planned |
| GW-4 | API integration with Backend-General | Planned |
| GW-5 | Static landing page | Planned |

---

## 3. Integration Contract

| Data | Source (Backend-General) | Status |
|------|--------------------------|--------|
| Auth (login/register) | `POST /api/auth/*` | available |
| Profile | WebSocket `get_profile` / REST | available |
| Match history | WebSocket `get_history` / REST | available |
| Leaderboard | `GET /api/admin/leaderboard` | available |
