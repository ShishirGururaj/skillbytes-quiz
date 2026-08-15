from fastapi import APIRouter, Depends

from app.database import get_database
from app.schemas.analytics import (
    FatigueWindow,
    LearningVelocity,
    QuestionDifficulty,
)
from app.services.analytics_service import (
    get_fatigue_analysis,
    get_learning_velocity,
    get_question_difficulty,
)


router = APIRouter(
    prefix="/api/analytics",
    tags=["Analytics"],
)


@router.get(
    "/learning-velocity",
    response_model=list[LearningVelocity],
)
def learning_velocity(
    database=Depends(get_database),
):
    return get_learning_velocity(database)


@router.get(
    "/fatigue/{user_id}/{quiz_id}",
    response_model=list[FatigueWindow],
)
def fatigue_analysis(
    user_id: str,
    quiz_id: str,
    database=Depends(get_database),
):
    return get_fatigue_analysis(
        database,
        user_id,
        quiz_id,
    )


@router.get(
    "/question-difficulty",
    response_model=list[QuestionDifficulty],
)
def question_difficulty(
    database=Depends(get_database),
):
    return get_question_difficulty(database)