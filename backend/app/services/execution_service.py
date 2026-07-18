from sqlalchemy.orm import Session

from app.models.submission import Submission
from app.models.test_case import TestCase
from app.schemas.execution import ExecutionResponse
from app.services.code_execution_service import CodeExecutionService


def execute_submission(
    db: Session,
    submission_id: int,
    user_id: int,
) -> ExecutionResponse:
    """
    Execute a submission against all test cases.
    """

    submission = (
        db.query(Submission)
        .filter(Submission.id == submission_id)
        .first()
    )

    if submission is None:
        raise ValueError("Submission not found.")

    if submission.user_id != user_id:
        raise ValueError("You are not authorized to execute this submission.")

    if submission.language.lower() != "python":
        raise ValueError("Only Python execution is supported currently.")

    test_cases = (
        db.query(TestCase)
        .filter(TestCase.question_id == submission.question_id)
        .all()
    )

    if not test_cases:
        raise ValueError("No test cases found for this question.")

    passed = 0
    total = len(test_cases)

    final_stdout = ""
    final_stderr = ""
    execution_time = 0.0

    for test_case in test_cases:

        result = CodeExecutionService.run_python(
            source_code=submission.source_code,
            input_data=test_case.input_data,
        )

        execution_time += result["execution_time"]

        final_stdout = result["stdout"]
        final_stderr = result["stderr"]

        if result["return_code"] != 0:
            submission.status = "Runtime Error"
            db.commit()

            return ExecutionResponse(
                submission_id=submission.id,
                status=submission.status,
                stdout=result["stdout"],
                stderr=result["stderr"],
                execution_time=execution_time,
            )

        if result["stdout"].strip() == test_case.expected_output.strip():
            passed += 1

    if passed == total:
        submission.status = "Accepted"
    else:
        submission.status = "Wrong Answer"

    db.commit()
    db.refresh(submission)

    return ExecutionResponse(
        submission_id=submission.id,
        status=f"{submission.status} ({passed}/{total} test cases passed)",
        stdout=final_stdout,
        stderr=final_stderr,
        execution_time=round(execution_time, 4),
    )