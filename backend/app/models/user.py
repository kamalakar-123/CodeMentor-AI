from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


# Define the users table so SQLAlchemy can create it on startup.
class User(Base):
    # Name of the PostgreSQL table.
    __tablename__ = "users"

    # Primary key integer column; PostgreSQL will generate the value automatically.
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Full name stored as variable-length text with a reasonable length limit.
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Email stored as variable-length text, required, unique, and indexed for fast lookup.
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
