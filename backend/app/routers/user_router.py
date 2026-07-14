from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import (
    create_user,
    get_all_users,
    get_user_by_email,
    get_user_by_id,
)


router = APIRouter(tags=["users"])


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists.",
        )

    return create_user(db, user_data)


@router.get("/users", response_model=list[UserResponse])
def get_all_users_endpoint(db: Session = Depends(get_db)):
    return get_all_users(db)


@router.get("/users/{id}", response_model=UserResponse)
def get_user_by_id_endpoint(id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return user
