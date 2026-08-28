---
trigger: always_on
---

# Performance Rules

## General
1. Avoid unnecessary work in loops.
2. Avoid repeated expensive operations.
3. Cache when beneficial.
4. Avoid premature optimization.
5. Prevent obvious inefficiencies.

## Rust
- Profile before optimizing (`cargo flamegraph` or `puffin`).
- Use `cargo build --release` for benchmarks; debug builds are not representative.
- Avoid allocations in hot paths; use `Arena` or pre-allocated buffers.
- `Arc<Mutex<T>>` is not free; prefer `tokio::sync` primitives in async code.

## Godot (GDScript)
- Avoid `_process()` and `_physics_process()` for heavy work.
- Use `@static_unload` for large scenes.
- Pool objects instead of instantiating/destroying in loops.
- Use `culling` for off-screen nodes.

## Laravel (PHP)
- Use `SELECT` only needed columns.
- Index database queries.
- Cache heavy computations with `Cache::remember()`.
