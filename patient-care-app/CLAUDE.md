# Patient Care EMR Demo Application

## Overview
HIPAA-compliant Electronic Medical Records (EMR) demo application built with FastAPI + SQLite. This is a **demo/testing application** — not for production use.

## Tech Stack
- **FastAPI** — web framework (run from `backend/`)
- **SQLite** — database (zero setup, file-based)
- **Pydantic** — input validation
- **python-jose** — JWT authentication
- **bcrypt** — password hashing
- **cryptography (Fernet)** — AES encryption for PHI fields

## Quick Start
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with real secrets (see .env.example for generation commands)
python seed_data.py    # Creates DB + demo data, prints credentials
uvicorn app.main:app --reload
```

## Project Structure
```
backend/
  app/
    main.py          — App assembly, middleware, router registration
    config.py        — Settings from environment variables (no defaults for secrets)
    database.py      — SQLite connection + schema initialization
    encryption.py    — Fernet encrypt/decrypt helpers for PHI
    auth/            — JWT handler, RBAC permissions, auth dependencies
    middleware/       — Audit logging, global error handler
    routers/         — API endpoints (auth, providers, patients, visits, treatments, audit)
    schemas/         — Pydantic request/response models
  seed_data.py       — Demo data seeder
```

## HIPAA Security Features
1. **Audit Logging** — Every CRUD operation logged with who/what/when/where/outcome
2. **RBAC** — Role-based access control (admin/provider/nurse) enforced via FastAPI dependencies
3. **PHI Encryption** — Patient PII, visit notes, diagnoses encrypted at rest with Fernet (AES)
4. **JWT Auth** — 30-minute token expiration (HIPAA auto-logoff), bcrypt password hashing
5. **Input Validation** — Pydantic schemas with max_length, regex patterns, type constraints
6. **Parameterized SQL** — All queries use parameterized statements (no string interpolation)
7. **Error Sanitization** — Global exception handler returns generic messages, never leaks PHI

## API Endpoints
- `POST /auth/login` — Get JWT token
- `/providers` — CRUD (admin-managed, self-update for providers)
- `/patients` — CRUD with PHI encryption (nurse: create/read only)
- `/visits` — CRUD with encrypted notes/diagnosis
- `/treatments` — CRUD with encrypted notes
- `/audit/logs` — Admin-only audit log query with filtering

## Roles & Permissions
- **admin** — Full access to everything including audit logs
- **provider** — Clinical CRUD, self-management, no audit access
- **nurse** — Read + create patients/visits, read treatments only

## Development Notes
- Database file: `backend/patient_care.db` (gitignored)
- All timestamps are ISO8601 UTC
- Soft deletes: `is_active` flag on providers/patients, status changes on visits/treatments
- Run from `backend/` directory for correct module resolution
