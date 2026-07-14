from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.question import QuestionCreate, QuestionResponse, QuestionUpdate
from app.services.question_service import (
    create_question,
    delete_question,
    get_all_questions,
    get_question_by_id,
    update_question,
)


router = APIRouter(tags=["questions"])


@router.post("/questions", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
def create_question_endpoint(question_data: QuestionCreate, db: Session = Depends(get_db)):
    return create_question(db, question_data)


@router.get("/questions", response_model=list[QuestionResponse])
def get_all_questions_endpoint(db: Session = Depends(get_db)):
    return get_all_questions(db)


@router.get("/questions/{id}", response_model=QuestionResponse)
def get_question_by_id_endpoint(id: int, db: Session = Depends(get_db)):
    question = get_question_by_id(db, id)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    return question


@router.put("/questions/{id}", response_model=QuestionResponse)
def update_question_endpoint(id: int, question_data: QuestionUpdate, db: Session = Depends(get_db)):
    question = update_question(db, id, question_data)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    return question


@router.delete("/questions/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question_endpoint(id: int, db: Session = Depends(get_db)):
    deleted = delete_question(db, id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
