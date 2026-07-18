from os import getenv
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")


def get_database_url() -> str:
    database_url = getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL is not set in the backend .env file.")
    return database_url


def get_secret_key() -> str:
    return getenv("SECRET_KEY", "change-this-secret-key-in-production")


def get_access_token_expire_minutes() -> int:
    return int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


def get_gemini_api_key() -> str:
    api_key = getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in the backend .env file.")
    return api_key


def get_gemini_model() -> str:
    model = getenv("GEMINI_MODEL")
    if not model:
        raise ValueError("GEMINI_MODEL is not set in the backend .env file.")
    return model