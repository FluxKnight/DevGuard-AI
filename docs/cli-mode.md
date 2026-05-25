# DevGuard AI CLI Mode

CLI Mode allows DevGuard AI to scan code files without starting the FastAPI server.

## Basic Usage

```bash
cd backend
python devguard_cli.py sample_vulnerable_login.py
```

## JSON Output

```bash
python devguard_cli.py sample_vulnerable_login.py --json
```

## Markdown Output

```bash
python devguard_cli.py sample_vulnerable_login.py --markdown
```

## Why CLI Mode Exists

API Mode is useful for backend demos and frontend integration.

CLI Mode is useful for quick local developer checks. It makes DevGuard AI closer to a real developer security tool.
