from datetime import datetime, timedelta, timezone

from app.services.analytics_service import (
    get_fatigue_analysis,
    get_learning_velocity,
    get_question_difficulty,
)


def test_learning_velocity(database):
    now = datetime.now(timezone.utc)

    database.attempts.insert_many(
        [
            {
                "user_id": "test_user",
                "quiz_id": "test_quiz",
                "question_id": "q1",
                "response_duration_seconds": 5,
                "is_correct": True,
                "question_shown_at": now,
            },
            {
                "user_id": "test_user",
                "quiz_id": "test_quiz",
                "question_id": "q2",
                "response_duration_seconds": 7,
                "is_correct": False,
                "question_shown_at": now,
            },
        ]
    )

    results = get_learning_velocity(database)

    assert len(results) == 1
    assert results[0]["user_id"] == "test_user"
    assert results[0]["accuracy"] == 50.0


def test_question_difficulty(database):
    now = datetime.now(timezone.utc)

    database.attempts.insert_many(
        [
            {
                "user_id": "user_a",
                "quiz_id": "quiz_a",
                "question_id": "q1",
                "response_duration_seconds": 5,
                "is_correct": True,
                "question_shown_at": now,
            },
            {
                "user_id": "user_b",
                "quiz_id": "quiz_a",
                "question_id": "q1",
                "response_duration_seconds": 10,
                "is_correct": False,
                "question_shown_at": now,
            },
        ]
    )

    results = get_question_difficulty(database)

    assert len(results) == 1
    assert results[0]["question_id"] == "q1"
    assert results[0]["total_attempts"] == 2
    assert results[0]["accuracy_percentage"] == 50.0


def test_fatigue_analysis(database):
    now = datetime.now(timezone.utc)

    attempts = []

    for index in range(10):
        attempts.append(
            {
                "user_id": "test_user",
                "quiz_id": "test_quiz",
                "question_id": f"q{index}",
                "response_duration_seconds": 5 + index,
                "is_correct": index < 5,
                "question_shown_at": now
                + timedelta(seconds=index),
            }
        )

    database.attempts.insert_many(attempts)

    results = get_fatigue_analysis(
        database,
        "test_user",
        "test_quiz",
    )

    assert len(results) == 2
    assert results[0]["window_start"] == 1
    assert results[0]["window_end"] == 5
    assert results[1]["window_start"] == 6
    assert results[1]["window_end"] == 10