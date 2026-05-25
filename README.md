# DevGuard AI

DevGuard AI is an AI-style code security reviewer backend built with FastAPI.

It scans source code for common security risks and returns structured findings, risk levels, explanations, and fix recommendations.

## Why I Built This

Many beginner developers accidentally push secrets, weak passwords, or unsafe code patterns into their projects. I built DevGuard AI as an educational security reviewer that helps developers understand risky code before it becomes a real problem.

The goal is not to replace professional security tools. The goal is to create a simple AI-assisted developer tool that explains security issues clearly.

## Features

- Analyze pasted source code
- Detect hardcoded passwords
- Detect possible API keys and tokens
- Detect weak password examples
- Detect SQL injection-style patterns
- Detect unsafe shell execution
- Detect debug mode configuration
- Detect insecure hash usage
- Generate risk score from 0 to 100
- Classify risk as LOW, MEDIUM, HIGH, or CRITICAL
- Store review history in SQLite
- Generate Markdown security reports

## Tech Stack

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- Regex-based scanner
- Template-based AI-style explanations

## API Endpoints

```txt
GET  /api/v1/health
POST /api/v1/reviews
GET  /api/v1/reviews
GET  /api/v1/reviews/{review_id}
GET  /api/v1/reports/{review_id}/markdown
```

## Local Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

```txt
http://127.0.0.1:8000/docs
```

## Deploy on Render

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

After deployment, open:

```txt
https://your-render-service-url.onrender.com/docs
```

## Example Request

```json
{
  "filename": "login.py",
  "language": "python",
  "code": "password = \"admin123\"\nquery = \"SELECT * FROM users WHERE name = \" + username\ndebug = True"
}
```

## Portfolio Story

DevGuard AI is my backend-focused AI engineering and cybersecurity project. It analyzes source code for common security risks, explains issues in human language, and generates safer recommendations.

I built it to show that I can design APIs, structure backend services, create rule-based analysis systems, and apply cybersecurity thinking to developer tools.
