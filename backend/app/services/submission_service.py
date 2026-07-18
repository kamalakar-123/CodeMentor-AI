from typing import Optional

from sqlalchemy.orm import Session

from app.models.question import Question
from app.models.submission import Submission
from app.models.user import User
from app.schemas.submission import SubmissionCreate


def create_submission(
    db: Session,
    user_id: int,
    submission_data: SubmissionCreate,
) -> Submission:
    """
    Create a new code submission.
    """

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found.")

    question = (
        db.query(Question)
        .filter(Question.id == submission_data.question_id)
        .first()
    )
    if not question:
        raise ValueError("Question not found.")

    submission = Submission(
        user_id=user_id,
        question_id=submission_data.question_id,
        language=submission_data.language,
        source_code=submission_data.source_code,
        status="Pending",
    )

    db.add(submission)
    db.commit()
    db.refresh(submission)

    return submission


def get_submission_by_id(
    db: Session,
    submission_id: int,
) -> Optional[Submission]:
    return (
        db.query(Submission)
        .filter(Submission.id == submission_id)
        .first()
    )


def get_user_submissions(
    db: Session,
    user_id: int,
) -> list[Submission]:
    return (
        db.query(Submission)
        .filter(Submission.user_id == user_id)
        .order_by(Submission.created_at.desc())
        .all()
    )


def get_question_submissions(
    db: Session,
    question_id: int,
) -> list[Submission]:
    return (
        db.query(Submission)
        .filter(Submission.question_id == question_id)
        .order_by(Submission.created_at.desc())
        .all()
    )