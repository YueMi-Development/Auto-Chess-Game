---
trigger: always_on
---

# Security Rules

## Secrets
- Never hardcode credentials or keys.
- Use environment variables or secure vaults.
- `.env` files are private; never commit them.
- Use `.env.example` with placeholder values only.

## Open Source (Root Repo)
- Root repo is open source: no internal hostnames, API keys, tokens, or private URLs.
- No references to `yuemi.my.id`, `forgejo.*`, `backend-general:8081`, or similar internal addresses.
- Submodule internals are private by definition (private repos).

## Input Validation
- Validate all user input.
- Sanitize input before use in critical contexts (DB, commands, etc.).

## Authentication & Authorization
- Check user permissions for every sensitive action.
- Fail securely (deny by default).

## Error Handling
- Avoid leaking sensitive info in errors.
- Log internally, but give generic messages externally.

## Dependencies
- Keep third-party libraries updated.
- Audit for known vulnerabilities:
  - Rust: `cargo audit`
  - PHP/Laravel: `composer audit`
  - Godot: monitor engine releases

## Data Safety
- Encrypt sensitive data at rest and in transit.
- Avoid logging PII.
- Never log credentials, tokens, or keys.

## Security Mindset
- Assume external input is malicious.
- Always follow the principle of least privilege.
