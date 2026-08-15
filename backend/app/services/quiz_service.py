from datetime import datetime, timezone

from bson import ObjectId
from fastapi import HTTPException
from pymongo.database import Database

from app.schemas.quiz import AnswerSubmission


def get_quiz_questions(
    database: Database,
    chapter_id: str,
    user_id: str,
) -> list[dict]:
    questions = list(
        database.questions.find(
            {"chapter_id": chapter_id},
            {
                "_id": 0,
                "question_id": 1,
                "text": 1,
                "options": 1,
            },
        ).sort("question_id", 1)
    )

    return [
        {
            **question,
            "position": index + 1,
        }
        for index, question in enumerate(questions)
    ]


def submit_answer(
    database: Database,
    submission: AnswerSubmission,
) -> dict:
    question = database.questions.find_one(
        {"question_id": submission.question_id}
    )

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found",
        )

    already_answered = database.attempts.find_one(
        {
            "user_id": submission.user_id,
            "quiz_id": submission.quiz_id,
            "question_id": submission.question_id,
        }
    )

    if already_answered:
        raise HTTPException(
            status_code=409,
            detail="Question has already been answered",
        )

    submitted_at = datetime.now(timezone.utc)

    shown_at = submission.question_shown_at
    response_duration = max(
        0.0,
        (submitted_at - shown_at).total_seconds(),
    )

    is_correct = (
        submission.selected_option == question["correct_option"]
    )

    attempt = {
        "user_id": submission.user_id,
        "quiz_id": submission.quiz_id,
        "question_id": submission.question_id,
        "exam_id": question["exam_id"],
        "subject_id": question["subject_id"],
        "chapter_id": question["chapter_id"],
        "question_shown_at": shown_at,
        "answer_submitted_at": submitted_at,
        "response_duration_seconds": response_duration,
        "selected_option": submission.selected_option,
        "is_correct": is_correct,
    }

    database.attempts.insert_one(attempt)

    return {
        "question_id": submission.question_id,
        "selected_option": submission.selected_option,
        "correct": is_correct,
        "response_duration_seconds": response_duration,
    }


def get_quiz_result(
    database: Database,
    quiz_id: str,
    user_id: str,
) -> dict:
    attempts = list(
        database.attempts.find(
            {
                "user_id": user_id,
                "quiz_id": quiz_id,
            }
        )
    )

    total = len(attempts)
    correct = sum(
        1 for attempt in attempts if attempt["is_correct"]
    )

    percentage = (
        round((correct / total) * 100, 2)
        if total
        else 0.0
    )

    return {
        "quiz_id": quiz_id,
        "user_id": user_id,
        "total_questions": total,
        "correct_answers": correct,
        "score_percentage": percentage,
    }  