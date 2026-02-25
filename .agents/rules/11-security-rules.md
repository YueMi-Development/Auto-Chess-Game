---
trigger: always_on
---

# Security Rules

## Secrets
- Never hardcode credentials or keys.
- Use environment variables or secure vaults.

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
- Audit for known vulnerabilities.

## Data Safety
- Encrypt sensitive data at rest and in transit.
- Avoid logging PII.

## Security Mindset
- Assume external input is malicious.
- Always follow the principle of least privilege.