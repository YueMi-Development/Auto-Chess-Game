---
trigger: always_on
---

# Architecture Rules

## General
1. Separate logic from IO.
2. Avoid global mutable state.
3. Avoid tight coupling.
4. Prefer modular design.
5. No hidden dependencies.
6. No God objects.

## Rust
- Use `async/await` with `tokio` for concurrency.
- Wrap errors with `anyhow` for application errors, `thiserror` for library errors.
- Use traits for abstraction, not concrete types.

## Submodule Monorepo
- Root repo is open source; submodules are private.
- `Documentation/PRD/` holds all component PRDs, symlinked from each submodule.
- `Backend/Shared-Files/proto/` holds shared proto definitions.
- CI workflow lives in root `.github/workflows/`.
- Shared secrets/credentials flow through Admin Panel only; never commit secrets to any repo.
