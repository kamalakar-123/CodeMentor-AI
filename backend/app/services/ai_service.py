from sqlalchemy.orm import Session

from app.ai.gemini_service import generate_question
from app.models.question import Question
from app.schemas.ai import GenerateQuestionRequest


def generate_and_save_question(
    db: Session,
    request: GenerateQuestionRequest,
) -> Question:
    """
    Generate a question using Gemini and save it to the database.
    Prevent duplicate questions based on title, language and difficulty.
    """

    generated_question = generate_question(
        language=request.language,
        difficulty=request.difficulty,
        question_type=request.question_type,
    )

    existing_question = (
        db.query(Question)
        .filter(
            Question.title == generated_question["title"],
            Question.language == request.language,
            Question.difficulty == request.difficulty,
        )
        .first()
    )

    if existing_question:
        return existing_question

    new_question = Question(
        title=generated_question["title"],
        description=generated_question["description"],
        difficulty=request.difficulty,
        language=request.language,
        question_type=request.question_type,
        starter_code=generated_question.get("starter_code", ""),
        expected_output=generated_question.get("expected_output", ""),
        explanation=generated_question.get("explanation", ""),
        ai_generated=True,
    )

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return new_question