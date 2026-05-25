# API Design

## Health

`GET /api/v1/health`

Returns service status.

## Create Review

`POST /api/v1/reviews`

Request:

```json
{
  "filename": "login.py",
  "language": "python",
  "code": "password = \"admin123\""
}
```

Response:

```json
{
  "review_id": 1,
  "filename": "login.py",
  "language": "python",
  "risk_level": "HIGH",
  "score": 65,
  "findings": [],
  "summary": "..."
}
```

## List Reviews

`GET /api/v1/reviews`

## Read Review

`GET /api/v1/reviews/{review_id}`

## Markdown Report

`GET /api/v1/reports/{review_id}/markdown`
