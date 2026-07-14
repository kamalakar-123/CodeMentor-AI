from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.models
from app.database import Base, engine
from app.api.home import router as home_router
from app.routers.user_router import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables during startup so PostgreSQL is ready before requests arrive.
    Base.metadata.create_all(bind=engine)
    yield


# Create the FastAPI application object that starts the server.
app = FastAPI(
    title="CodeMentor AI API",
    version="0.3.0",
    description="Backend API for CodeMentor AI, an AI-powered coding interview preparation platform.",
    lifespan=lifespan,
)


# Allow the React app on localhost:5173 to call the backend during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register the route collection that lives in app/api/home.py.
app.include_router(home_router)


# Register user management routes.
app.include_router(user_router)
