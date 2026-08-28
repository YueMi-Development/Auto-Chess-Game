---
trigger: always_on
---

# Style Rules

## Consistency
One formatting style across entire project.

## Rust
- Run `cargo fmt` before committing.
- Run `cargo clippy -- -D warnings` before committing.
- No `unwrap()` in production code; use `?` or explicit `match`.

## Godot (GDScript)
- Use `@tool` sparingly; document when used.
- Signal declarations above variables, then functions.
- Use `const` for compile-time constants.

## Laravel (PHP)
- Follow PSR-12.
- Use Laravel conventions for naming controllers, models, migrations.
- No inline HTML in controllers.

## Control Flow
Always use explicit blocks.
No single-line condition shortcuts.

## Indentation
Consistent indentation.
No mixed styles.

## Spacing
Use spacing to separate logic.
No random vertical gaps.
