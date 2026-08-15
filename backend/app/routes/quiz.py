from fastapi import APIRouter, Depends

from app.database import get_database
from app.schemas.quiz import (
    AnswerSubmission,
    QuizResponse,
    QuizResult,
)
from app.services.quiz_service import (
    get_quiz_questions,
    get_quiz_result,
    submit_answer,
)


router = APIRouter(prefix="/api/quiz", tags=["Quiz"])


@router.get(
    "/{chapter_id}",
    response_model=QuizResponse,
)
def get_quiz(
    chapter_id: str,
    user_id: str,
    database=Depends(get_database),
):
    questions = get_quiz_questions(
        database,
        chapter_id,
        user_id,
    )

    return {
        "quiz_id": chapter_id,
        "user_id": user_id,
        "questions": questions,
    }


@router.post("/submit")
def submit_quiz_answer(
    submission: AnswerSubmission,
    database=Depends(get_database),
):
    return submit_answer(
        database,
        submission,
    )


@router.get(
    "/{quiz_id}/result",
    response_model=QuizResult,
)
def quiz_result(
    quiz_id: str,
    user_id: str,
    database=Depends(get_database),
):
    return get_quiz_result(
        database,
        quiz_id,
        user_id,
    )