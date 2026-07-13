from os import getenv
from pathlib import Path

from dotenv import load_dotenv


# Load environment variables from the backend .env file.
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")


# Return the database URL from the environment and fail fast if it is missing.
def get_database_url() -> str:
    database_url = getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL is not set in the backend .env file.")
    return database_url
