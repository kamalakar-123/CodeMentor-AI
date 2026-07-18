from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.execution import ExecutionResponse
from app.schemas.submission import (
    SubmissionCreate,
    SubmissionResponse,
)
from app.services.execution_service import execute_submission
from app.services.submission_service import (
    create_submission,
    get_question_submissions,
    get_submission_by_id,
    get_user_submissions,
)

router = APIRouter(
    prefix="/submissions",
    tags=["Submissions"],
)


@router.post(
    "",
    response_model=SubmissionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_submission_endpoint(
    submission_data: SubmissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return create_submission(
            db=db,
            user_id=current_user.id,
            submission_data=submission_data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/me",
    response_model=list[SubmissionResponse],
)
def get_my_submissions_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_submissions(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/{submission_id}",
    response_model=SubmissionResponse,
)
def get_submission_endpoint(
    submission_id: int,
    db: Session = Depends(get_db),
):
    submission = get_submission_by_id(
        db=db,
        submission_id=submission_id,
    )

    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found.",
        )

    return submission


@router.get(
    "/question/{question_id}",
    response_model=list[SubmissionResponse],
)
def get_question_submissions_endpoint(
    question_id: int,
    db: Session = Depends(get_db),
):
    return get_question_submissions(
        db=db,
        question_id=question_id,
    )


@router.post(
    "/{submission_id}/run",
    response_model=ExecutionResponse,
)
def run_submission_endpoint(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return execute_submission(
            db=db,
            submission_id=submission_id,
            user_id=current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc