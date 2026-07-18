from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.models
from app.database import Base, engine
from app.api.home import router as home_router
from app.routers.user_router import router as user_router
from app.routers.auth_router import router as auth_router
from app.routers.question_router import router as question_router
from app.routers.ai_router import router as ai_router
from app.routers.submission import router as submission_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables during startup so PostgreSQL is ready before requests arrive.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="CodeMentor AI API",
    version="0.5.0",
    description="Backend API for CodeMentor AI, an AI-powered coding interview preparation platform with Gemini integration.",
    lifespan=lifespan,
)


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


app.include_router(home_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(question_router)
app.include_router(ai_router)
app.include_router(submission_router)