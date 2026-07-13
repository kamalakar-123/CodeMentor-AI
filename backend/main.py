from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# Create the FastAPI application object.
app = FastAPI(
    title="CodeMentor AI API",
    version="0.1.0",
    description="Backend API for CodeMentor AI, an AI-powered coding interview preparation platform.",
)


# Allow the React frontend to call this backend during development.
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


# Return a welcome message from the root endpoint.
@app.get("/")
def read_root():
    return {"message": "Welcome to CodeMentor AI API"}


# Return a simple health check response.
@app.get("/health")
def health_check():
    return {"status": "ok"}
