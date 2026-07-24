# Daily Log

## Day 1 — Project Setup
- Set up Python virtual environments and PowerShell activation
- Established a layered backend structure (api/models/schemas/services/core)
- Configured .gitignore and initialized version control
- Commits: setup: initialize project structure and folder layout

## Day 2 — FastAPI Foundations
- Installed FastAPI and uvicorn; built the first live endpoints (/, /health)
- Resolved PowerShell encoding issues (UTF-16 vs UTF-8) affecting git diffs
- Fixed git commit author configuration
- Commits: feat: add first FastAPI endpoints (root and health check)

## Day 3 — Authentication
- Implemented password hashing (bcrypt/passlib) and resolved a version conflict
- Built JWT token generation with expiration handling
- Created register/login endpoints using Pydantic schemas and APIRouter
- Moved secrets to .env using pydantic-settings
- Added route protection via OAuth2PasswordBearer and Depends()
- Tested the full auth flow end-to-end (register, login, invalid credentials, protected routes)
- Commits: feat: add password hashing with bcrypt; feat: add JWT token generation; feat: move secrets to .env; feat: add protected route via JWT verification

## Day 4 — Database Integration
- Installed and configured PostgreSQL and pgAdmin
- Connected FastAPI to PostgreSQL via SQLAlchemy (engine, session, Base)
- Defined the User model and created the users table
- Migrated register/login from in-memory storage to PostgreSQL
- Hardened auth with password strength validation, email normalization, transaction rollback, and logging
- Commits: feat: connect FastAPI to PostgreSQL via SQLAlchemy; feat: define User model and create users table; feat: harden auth with validation, normalization, and logging

## Day 5 — Upload Module, GitHub, and Document Parsing
- Built the Document model with a foreign key to User and an enum-based status field
- Implemented a hardened file upload endpoint: content-type validation, size limits, UUID-based safe filenames
- Fixed Swagger UI's Authorize flow using HTTPBearer for simpler token testing
- Pushed the project to GitHub and set up remote tracking
- Identified and rotated an exposed secret in .env.example; used git filter-repo to remove it from commit history
- Installed Docling and ran the first real PDF parse
- Commits: feat: add Document model and safe file upload; fix: remove real secrets from .env.example; feat: install Docling for document parsing