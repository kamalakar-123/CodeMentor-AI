from typing import Optional

from sqlalchemy.orm import Session

from app.models.question import Question
from app.schemas.question import QuestionCreate, QuestionUpdate


def create_question(db: Session, question_data: QuestionCreate) -> Question:
    question = Question(**question_data.model_dump())
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


def get_all_questions(db: Session) -> list[Question]:
    return db.query(Question).order_by(Question.id.asc()).all()


def get_question_by_id(db: Session, question_id: int) -> Optional[Question]:
    return db.query(Question).filter(Question.id == question_id).first()


def update_question(db: Session, question_id: int, question_data: QuestionUpdate) -> Optional[Question]:
    question = get_question_by_id(db, question_id)
    if not question:
        return None

    for field, value in question_data.model_dump().items():
        setattr(question, field, value)

    db.commit()
    db.refresh(question)
    return question


def delete_question(db: Session, question_id: int) -> bool:
    question = get_question_by_id(db, question_id)
    if not question:
        return False

    db.delete(question)
    db.commit()
    return True
