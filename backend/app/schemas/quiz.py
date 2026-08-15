from datetime import datetime

from pydantic import BaseModel, Field


class AnswerSubmission(BaseModel):
    user_id: str
    quiz_id: str
    question_id: str
    selected_option: int = Field(ge=0, le=3)
    question_shown_at: datetime


class AnswerResult(BaseModel):
    question_id: str
    selected_option: int
    correct: bool
    response_duration_seconds: float


class QuizQuestion(BaseModel):
    question_id: str
    text: str
    options: list[str]
    position: int


class QuizResponse(BaseModel):
    quiz_id: str
    user_id: str
    questions: list[QuizQuestion]


class QuizResult(BaseModel):
    quiz_id: str
    user_id: str
    total_questions: int
    correct_answers: int
    score_percentage: float