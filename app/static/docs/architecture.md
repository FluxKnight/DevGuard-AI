# DevGuard AI Architecture

DevGuard AI is a backend-focused code security reviewer.

## Flow

1. Client sends source code to `POST /api/v1/reviews`
2. FastAPI validates the request with Pydantic
3. `CodeScanner` applies regex-based security rules
4. `risk_scoring.py` calculates score and risk level
5. `explanation.py` generates human-readable summary
6. SQLAlchemy stores review history in SQLite
7. Report endpoint generates Markdown output

## AI Layer Ready

The current MVP uses template-based explanations. A future AI explanation service can be added without changing the scanner or API contract.
