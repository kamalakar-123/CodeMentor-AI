# CodeMentor AI Backend - Day 2

This backend is organized as a small FastAPI application package.

## Folder Purpose

- `app/`: the Python package that contains the FastAPI application code.
- `app/api/`: route modules live here so HTTP endpoints stay separated by feature.
- `app/core/`: shared application configuration belongs here.
- `app/models/`: database models will go here later. It stays empty for Day 2.
- `app/schemas/`: request and response schemas will go here later. It stays empty for Day 2.
- `app/services/`: business logic and orchestration helpers belong here.
- `app/utils/`: reusable utility functions and helpers belong here.

## FastAPI Architecture

FastAPI applications usually work best when they are split into layers:

- the application entrypoint configures the server,
- routers define HTTP endpoints,
- schemas define data contracts,
- services hold business logic,
- models represent persistence later,
- utilities hold reusable helpers.

This keeps code easier to read, test, and extend.

## APIRouter

`APIRouter` is FastAPI's router object for grouping related endpoints.

We use it so the home routes live in `app/api/home.py` instead of being mixed into the app startup file.

## Run the backend

```powershell
cd backend
..\\.venv\\Scripts\\python.exe -m uvicorn app.main:app --reload
```

## Expected Endpoints

- `GET /api/`
- `GET /api/health`

## Common Errors

- `ModuleNotFoundError`: activate the virtual environment before running Uvicorn.
- `Address already in use`: stop anything already using port `8000`.
- `CORS error`: confirm the frontend runs from `http://localhost:5173`.
