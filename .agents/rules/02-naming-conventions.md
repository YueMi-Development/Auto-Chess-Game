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
  isValid
  hasPermission
  canExecute
  shouldRetry

## Constants
- Clearly distinguished.
- Immutable by intent.
- No magic values.