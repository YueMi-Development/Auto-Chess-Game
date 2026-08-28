---
trigger: always_on
---

# Agent Behavior Rules

When reviewing or generating code:

1. Enforce naming clarity.
2. Refactor large or messy functions.
3. Remove unnecessary complexity.
4. Enforce consistency.
5. Identify architectural flaws.
6. Reject unclear logic.
7. Be direct about design problems.
8. Always check which submodule scope you are operating in before editing.
9. Root-level changes must not expose private submodule internals.
10. When in doubt, ask before committing to a design decision.
11. Never commit secrets or credentials.
12. Run `cargo fmt && cargo clippy` before claiming Rust code is done.
