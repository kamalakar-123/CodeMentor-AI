# CodeMentor AI

CodeMentor AI is a Day 1 starter for an AI-powered coding interview preparation platform.

## What this project includes

- A FastAPI backend with `GET /` and `GET /health`.
- A Vite + React frontend that fetches the backend welcome message.
- CORS enabled so the browser can talk to the API during development.

## Project structure

```text
CodeMenter_AI/
├─ backend/
│  ├─ main.py
│  └─ requirements.txt
├─ frontend/
│  ├─ index.html
│  ├─ package.json
│  ├─ vite.config.js
│  ├─ .env.example
│  └─ src/
│     ├─ App.jsx
│     ├─ main.jsx
│     ├─ pages/
│     │  └─ Home.jsx
│     └─ styles.css
├─ .gitignore
└─ README.md
```

## Backend packages

- `fastapi`: the web framework used to build the API.
- `uvicorn[standard]`: the ASGI server used to run the FastAPI app in development.

## Frontend files

- `package.json`: defines the Vite app and its scripts.
- `index.html`: the HTML shell that Vite loads.
- `vite.config.js`: Vite configuration for React.
- `src/main.jsx`: React entry point.
- `src/App.jsx`: fetches backend data and manages loading/error state.
- `src/pages/Home.jsx`: renders the homepage UI.
- `src/styles.css`: simple production-friendly styling.

## Core concepts

### FastAPI

FastAPI is a modern Python web framework for building APIs quickly. It is fast, typed, easy to read, and automatically generates interactive API docs.

### React

React is a JavaScript library for building user interfaces. It lets you create reusable UI components and update the screen when data changes.

### CORS

CORS stands for Cross-Origin Resource Sharing. The browser blocks frontend code from calling a different origin unless the backend allows it. We enable CORS so the Vite app can call the FastAPI server during development.

### REST APIs

REST APIs are web APIs that expose resources through standard HTTP methods like `GET`, `POST`, `PUT`, and `DELETE`. They are simple, predictable, and easy to integrate with frontend apps.

### JSON

JSON is a lightweight text format for exchanging data. APIs often send JSON because it is easy for both Python and JavaScript to read.

## Run the backend

```powershell
cd backend
..\\.venv\\Scripts\\python.exe -m uvicorn main:app --reload
```

## Run the frontend

```powershell
cd frontend
npm install
npm run dev
```

## Expected output

- Backend root endpoint returns `{"message":"Welcome to CodeMentor AI API"}`.
- Backend health endpoint returns `{"status":"ok"}`.
- Frontend shows the CodeMentor AI title, a short subtitle, and the backend welcome message.

## Common errors

- `ModuleNotFoundError`: install backend dependencies inside the virtual environment with `pip install -r requirements.txt`.
- `Address already in use`: stop the process on port `8000` or `5173` and start again.
- `CORS error`: make sure the frontend is running on `http://localhost:5173` or `http://127.0.0.1:5173`.
- `fetch failed`: confirm the backend is running and the frontend API URL matches the backend host and port.
