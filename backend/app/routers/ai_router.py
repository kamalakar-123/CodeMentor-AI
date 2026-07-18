from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.ai.gemini_service import GeminiServiceError, generate_question
from app.database import get_db
from app.schemas.ai import (
    GenerateQuestionRequest,
    GenerateQuestionResponse,
)
from app.schemas.question import QuestionResponse
from app.services.ai_service import generate_and_save_question

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post(
    "/generate-question",
    response_model=GenerateQuestionResponse,
)
def generate_question_endpoint(request: GenerateQuestionRequest):
    try:
        question = generate_question(
            language=request.language,
            difficulty=request.difficulty,
            question_type=request.question_type,
        )

        return GenerateQuestionResponse(**question)

    except GeminiServiceError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@router.post(
    "/generate-and-save",
    response_model=QuestionResponse,
    status_code=201,
)
def generate_and_save_endpoint(
    request: GenerateQuestionRequest,
    db: Session = Depends(get_db),
):
    """
    Generate a coding question using Gemini AI and save it to PostgreSQL.
    If an identical question already exists, return the existing record.
    """
    try:
        question = generate_and_save_question(
            db=db,
            request=request,
        )

        return question

    except GeminiServiceError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc