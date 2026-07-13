from fastapi import APIRouter


# Create a router to keep the home endpoints grouped together.
router = APIRouter(prefix="/api", tags=["home"])


# Return a welcome message from the API root.
@router.get("/")
def read_root():
    return {"message": "Welcome to CodeMentor AI API"}


# Return a simple health check response for monitoring.
@router.get("/health")
def health_check():
    return {"status": "ok"}
