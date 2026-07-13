from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import get_database_url


# Read the PostgreSQL connection string from the environment.
DATABASE_URL = get_database_url()


# Create the SQLAlchemy engine, which manages database connections and pooling.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


# Create a session factory for database work; each request can create its own session.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# Create the shared base class that all SQLAlchemy models inherit from.
Base = declarative_base()
