from typing import Optional

from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserLogin, UserRegister
from app.services.user_service import get_user_by_email


def register_user(db: Session, user_data: UserRegister) -> User:
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise ValueError("A user with this email already exists.")

    user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        role="student",
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(
    db: Session,
    email: str | UserLogin,
    password: str | None = None,
) -> Optional[User]:
    # Keep compatibility with existing callers that pass a UserLogin object.
    if isinstance(email, UserLogin):
        user_login = email
        email_value = user_login.email
        password_value = user_login.password
    else:
        email_value = email
        password_value = password

    if password_value is None:
        return None

    user = get_user_by_email(db, email_value)
    if not user:
        return None
    if not verify_password(password_value, user.hashed_password):
        return None
    if not user.is_active:
        return None
    return user
