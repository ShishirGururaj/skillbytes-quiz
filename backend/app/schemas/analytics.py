from pydantic import BaseModel


class LearningVelocity(BaseModel):
    user_id: str
    accuracy: float
    avg_response_time: float
    consistency_score: float
    learning_velocity_index: float


class FatigueWindow(BaseModel):
    window_start: int
    window_end: int
    accuracy: float
    avg_response_time: float
    attempts: int


class QuestionDifficulty(BaseModel):
    question_id: str
    total_attempts: int
    accuracy_percentage: float
    avg_response_time: float
    difficulty_score: float