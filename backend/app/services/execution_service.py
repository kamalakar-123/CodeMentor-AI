from sqlalchemy.orm import Session

from app.models.question import Question
from app.models.submission import Submission
from app.schemas.execution import ExecutionResponse
from app.services.code_execution_service import CodeExecutionService


def execute_submission(
    db: Session,
    submission_id: int,
    user_id: int,
) -> ExecutionResponse:
    """
    Execute a user's submission and compare its output
    with the expected output.
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

    question = (
        db.query(Question)
        .filter(Question.id == submission.question_id)
        .first()
    )

    if question is None:
        raise ValueError("Question not found.")

    result = CodeExecutionService.run_python(submission.source_code)

    stdout = result["stdout"].strip()
    stderr = result["stderr"].strip()
    expected_output = (question.expected_output or "").strip()

    # Debug (remove later if desired)
    print("\n" + "=" * 60)
    print(f"Submission ID : {submission.id}")
    print(f"Question ID   : {question.id}")
    print(f"Return Code   : {result['return_code']}")
    print(f"STDOUT        : {repr(stdout)}")
    print(f"STDERR        : {repr(stderr)}")
    print(f"Expected      : {repr(expected_output)}")
    print("=" * 60 + "\n")

    if result["return_code"] != 0:
        submission.status = "Runtime Error"
    elif stdout == expected_output:
        submission.status = "Accepted"
    else:
        submission.status = "Wrong Answer"

    db.commit()
    db.refresh(submission)

    return ExecutionResponse(
        submission_id=submission.id,
        status=submission.status,
        stdout=result["stdout"],
        stderr=result["stderr"],
        execution_time=result["execution_time"],
    )