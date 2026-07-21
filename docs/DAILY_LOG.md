# Daily Log

## Day 1 — Project Setup
- Worked on: virtual environments (venv), PATH mechanics, PowerShell activation
- Worked on: layered folder structure (api/models/schemas/services/core) and why each layer is separated
- Worked on: .gitignore mechanics and why venv should never be committed
- Commits: setup: initialize project structure and folder layout

## Day 2 — FastAPI Foundations
- Worked on: installing FastAPI + uvicorn, understanding ASGI servers vs frameworks
- Worked on: first live endpoint (`/`, `/health`), uvicorn reload workflow
- Worked on: debugging PowerShell encoding issues (UTF-16 vs UTF-8 vs ASCII) breaking git diffs
- Worked on: fixing git commit author email configuration
- Commits: feat: add first FastAPI endpoints (root and health check)

## Day 3 — Authentication Core
- Worked on: password hashing with bcrypt/passlib, why slow hashing matters for passwords
- Worked on: debugging a real bcrypt/passlib version conflict (pinned bcrypt==4.0.1)
- Worked on: JWT token generation, token structure (header/payload/signature), expiration handling
- Worked on: Pydantic schemas, APIRouter, building real /auth/register and /auth/login endpoints
- Worked on: moving secrets out of source code into .env with pydantic-settings, generating a secure key
- Commits: feat: add password hashing with bcrypt, pin compatible bcrypt version; feat: add JWT token generation with expiration; feat: move secrets to .env, add pydantic-settings config; chore: update requirements.txt with pydantic-settings and python-dotenv