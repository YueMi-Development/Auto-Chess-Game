---
trigger: always_on
---

# Error Handling

## General
1. Never silently ignore errors.
2. Provide meaningful error messages.
3. Propagate errors when appropriate.
4. Add context when rethrowing.
5. Fail fast on invalid states.

## Rust
- Use `Result<T, E>` for fallible operations.
- Use `anyhow::Result<T>` in binaries and tests.
- Use `thiserror` to define error types in libraries.
- Never use `unwrap()` or `expect()` in production paths.
- Use `?` operator to propagate errors cleanly.
- Log errors with `tracing::error!` at the boundary.

## Godot (GDScript)
- Use `push_error()` and `push_warning()` for debug output.
- Return `null` or `-1` for error states; document return values.
- Use `@export` annotations for configuration.

## Laravel (PHP)
- Use `try/catch` sparingly; prefer framework validation.
- Throw `ValidationException`, not generic exceptions.
- Log with `Log::error()`.
