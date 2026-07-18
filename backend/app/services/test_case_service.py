from sqlalchemy.orm import Session

from app.models.question import Question
from app.models.test_case import TestCase
from app.schemas.test_case import (
    TestCaseCreate,
    TestCaseUpdate,
)


def create_test_case(
    db: Session,
    test_case_data: TestCaseCreate,
) -> TestCase:
    """
    Create a new test case for a question.
    """

    question = (
        db.query(Question)
        .filter(Question.id == test_case_data.question_id)
        .first()
    )

    if question is None:
        raise ValueError("Question not found.")

    test_case = TestCase(
        question_id=test_case_data.question_id,
        input_data=test_case_data.input_data,
        expected_output=test_case_data.expected_output,
        is_hidden=test_case_data.is_hidden,
    )

    db.add(test_case)
    db.commit()
    db.refresh(test_case)

    return test_case


def get_test_case_by_id(
    db: Session,
    test_case_id: int,
) -> TestCase | None:
    return (
        db.query(TestCase)
        .filter(TestCase.id == test_case_id)
        .first()
    )


def get_test_cases_by_question(
    db: Session,
    question_id: int,
) -> list[TestCase]:
    return (
        db.query(TestCase)
        .filter(TestCase.question_id == question_id)
        .all()
    )


def update_test_case(
    db: Session,
    test_case_id: int,
    test_case_data: TestCaseUpdate,
) -> TestCase:
    test_case = get_test_case_by_id(
        db=db,
        test_case_id=test_case_id,
    )

    if test_case is None:
        raise ValueError("Test case not found.")

    update_data = test_case_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(test_case, field, value)

    db.commit()
    db.refresh(test_case)

    return test_case


def delete_test_case(
    db: Session,
    test_case_id: int,
) -> None:
    test_case = get_test_case_by_id(
        db=db,
        test_case_id=test_case_id,
    )

    if test_case is None:
        raise ValueError("Test case not found.")

    db.delete(test_case)
    db.commit()