---
trigger: always_on
---

# Structure Rules

## Single Responsibility
Each function/module does one thing only.

## Function Size
Small and focused.
If hard to name — split it.

## Parameters
Limit parameter count.
If too many — group into structured object.

## File Responsibility
One clear responsibility per file/module.

## Rust Crate Structure
```
src/
  main.rs          # binary entry point only
  lib.rs           # re-exports, public types
  <module>/        # one module per concern
```

## Godot Scene Structure
One scene per responsibility.
Autoloads for singletons only.
Scripts co-located with their scene.

## Submodule Scope
Do not import or reference private submodule internals from root-level docs or CI.
Root docs must be readable without access to private submodules.
