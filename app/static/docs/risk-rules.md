# Risk Rules

## MVP Detection Rules

1. Hardcoded passwords
2. Possible API keys and tokens
3. Weak passwords
4. SQL injection-style string building
5. Debug mode enabled
6. Environment file references
7. Unsafe shell execution
8. Insecure hash algorithms

## Severity Points

- LOW: 10
- MEDIUM: 25
- HIGH: 40
- CRITICAL: 60

The score is capped at 100.
