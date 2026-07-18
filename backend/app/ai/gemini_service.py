import json
import re
from typing import Any

from google import genai
from google.genai import types

from app.config import get_gemini_api_key, get_gemini_model


class GeminiServiceError(Exception):
    pass


def _build_prompt(language: str, difficulty: str, question_type: str) -> str:
    return f"""
Generate one {question_type} interview question.

Programming Language: {language}
Difficulty: {difficulty}

Return only valid JSON with exactly these keys:

{{
  "title": "",
  "description": "",
  "starter_code": "",
  "expected_output": "",
  "explanation": ""
}}

Do not include markdown, code fences, or extra text.
""".strip()


def _extract_json_payload(text: str) -> str:
    cleaned_text = text.strip()
    if cleaned_text.startswith("```"):
        cleaned_text = re.sub(
            r"^```(?:json)?\s*|\s*```$",
            "",
            cleaned_text,
            flags=re.IGNORECASE | re.DOTALL,
        ).strip()
    return cleaned_text


def _validate_response_payload(payload: Any) -> dict[str, str]:
    required_fields = [
        "title",
        "description",
        "starter_code",
        "expected_output",
        "explanation",
    ]

    if not isinstance(payload, dict):
        raise GeminiServiceError("Gemini returned an invalid response payload.")

    missing_fields = [field for field in required_fields if field not in payload]
    if missing_fields:
        raise GeminiServiceError(
            f"Gemini response is missing fields: {', '.join(missing_fields)}"
        )

    return {
        field: str(payload.get(field, "")).strip()
        for field in required_fields
    }


def generate_question(
    language: str,
    difficulty: str,
    question_type: str,
) -> dict[str, str]:
    prompt = _build_prompt(language, difficulty, question_type)

    try:
        client = genai.Client(api_key=get_gemini_api_key())
        response = client.models.generate_content(
            model=get_gemini_model(),
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                response_mime_type="application/json",
            ),
        )
    except Exception as exc:
        raise GeminiServiceError(f"Gemini request failed: {exc}") from exc

    response_text = getattr(response, "text", None)
    if not response_text:
        raise GeminiServiceError("Gemini returned an empty response.")

    try:
        payload = json.loads(_extract_json_payload(response_text))
    except json.JSONDecodeError as exc:
        raise GeminiServiceError("Gemini returned invalid JSON.") from exc

    return _validate_response_payload(payload)