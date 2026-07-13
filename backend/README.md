# CodeMentor AI Backend - Day 3

This backend now connects FastAPI to PostgreSQL through SQLAlchemy while keeping the existing API routes intact.

## Folder Purpose

- `app/`: the main Python package for the backend.
- `app/api/`: HTTP routes live here, grouped by feature.
- `app/core/`: reserved for shared core settings later.
- `app/models/`: SQLAlchemy models that map Python classes to PostgreSQL tables.
- `app/schemas/`: reserved for request and response schemas later.
- `app/services/`: reserved for business logic later.
- `app/utils/`: reserved for reusable helper functions later.

## FastAPI And PostgreSQL Flow

FastAPI handles web requests, and SQLAlchemy handles database communication.

At startup, `app/main.py` imports the model package so SQLAlchemy knows about the table metadata, then `Base.metadata.create_all(bind=engine)` creates any missing tables in PostgreSQL.

## APIRouter

`APIRouter` groups related routes together so `app/main.py` stays small and focused on application setup.

## Run The Backend

```powershell
cd backend
..\\.venv\\Scripts\\python.exe -m uvicorn app.main:app --reload
```

## Verify PostgreSQL

1. Open pgAdmin.
2. Connect to your local PostgreSQL server.
3. Expand `Databases` > `codementor_ai` > `Schemas` > `public` > `Tables`.
4. Confirm the `users` table exists.
5. Open the Query Tool and run:

```sql
SELECT * FROM users;
```

## Expected Endpoints

- `GET /api/`
- `GET /api/health`

## Common Errors

- `DATABASE_URL is not set`: check the backend `.env` file.
- `password authentication failed`: replace `YOUR_PASSWORD` with the real PostgreSQL password.
- `could not connect to server`: confirm PostgreSQL is running on port `5432`.
- `ModuleNotFoundError`: activate the virtual environment before running Uvicorn.
- `Address already in use`: stop anything already using port `8000`.
- `CORS error`: confirm the frontend runs from `http://localhost:5173`.
