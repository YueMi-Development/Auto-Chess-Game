---
trigger: always_on
---

# Naming Conventions

## Variables
- Descriptive names only.
- Full words preferred over abbreviations.
- No meaningless names (x, tmp, data).

## Functions
- Must start with a verb.
- Clearly describe action.
- No vague names like doStuff or handleData.

## Booleans
- Must read naturally:
  - `is_valid`, `has_permission`, `can_execute`, `should_retry`

## Rust
- Use `snake_case` for variables, functions, modules.
- Use `PascalCase` for types, enums, traits.
- Use `SCREAMING_SNAKE_CASE` for constants.

## Godot (GDScript)
- Use `snake_case` for variables and functions.
- Use `PascalCase` for classes and nodes.
- Signal names: `snake_case` with past tense, e.g. `player_connected`, `health_depleted`.

## Constants
- Clearly distinguished.
- Immutable by intent.
- No magic values.
