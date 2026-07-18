from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.test_case import (
    TestCaseCreate,
    TestCaseResponse,
    TestCaseUpdate,
)
from app.services.test_case_service import (
    create_test_case,
    delete_test_case,
    get_test_case_by_id,
    get_test_cases_by_question,
    update_test_case,
)

router = APIRouter(
    prefix="/test-cases",
    tags=["Test Cases"],
)


@router.post(
    "",
    response_model=TestCaseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_test_case_endpoint(
    test_case_data: TestCaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return create_test_case(db, test_case_data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/{test_case_id}",
    response_model=TestCaseResponse,
)
def get_test_case_endpoint(
    test_case_id: int,
    db: Session = Depends(get_db),
):
    test_case = get_test_case_by_id(db, test_case_id)

    if test_case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test case not found.",
        )

    return test_case


@router.get(
    "/question/{question_id}",
    response_model=list[TestCaseResponse],
)
def get_test_cases_by_question_endpoint(
    question_id: int,
    db: Session = Depends(get_db),
):
    return get_test_cases_by_question(db, question_id)


@router.put(
    "/{test_case_id}",
    response_model=TestCaseResponse,
)
def update_test_case_endpoint(
    test_case_id: int,
    test_case_data: TestCaseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return update_test_case(
            db,
            test_case_id,
            test_case_data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{test_case_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_test_case_endpoint(
    test_case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        delete_test_case(db, test_case_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc