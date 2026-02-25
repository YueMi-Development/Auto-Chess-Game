---
trigger: always_on
---

# Testing Rules

## Coverage
- Critical logic must be tested.
- Prefer unit tests for pure functions.
- Integration tests for system interactions.
- End-to-end tests for full workflows.

## Test Naming
- Describe intent, not implementation.
- Example: testCalculateTotal_withNegativeInput_returnsZero

## Test Quality
- Avoid fragile tests that break on minor changes.
- Each test should have **one assertion focus**.
- Use mocks/stubs only where necessary.

## Automation
- All tests must run automatically in CI.
- Failures must block merges.

## Testable Design
- Code should be **designed for testability**.
- Avoid hard-to-mock static/global dependencies.
- Separate side-effects from logic.