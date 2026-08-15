import random
from datetime import datetime, timedelta, timezone

from app.database import db


def generate_demo_attempts() -> None:
    random.seed(42)

    db.attempts.delete_many({})

    users = [
        "user_001",
        "user_002",
        "user_003",
        "user_004",
        "user_005",
    ]

    questions = list(
        db.questions.find(
            {},
            {
                "_id": 0,
                "question_id": 1,
                "exam_id": 1,
                "subject_id": 1,
                "chapter_id": 1,
                "correct_option": 1,
            },
        ).limit(100)
    )

    if not questions:
        raise RuntimeError("No questions found. Run seed.py first.")

    now = datetime.now(timezone.utc)

    attempts = []

    for user_index, user_id in enumerate(users):
        user_questions = questions[
            user_index * 20 : (user_index + 1) * 20
        ]

        for position, question in enumerate(user_questions):
            shown_at = now - timedelta(
                minutes=(20 - position) * 3
            )

            # Each user has a different performance profile.
            if user_id == "user_001":
                accuracy_probability = 0.90
                base_response_time = 3.0
            elif user_id == "user_002":
                accuracy_probability = 0.75
                base_response_time = 5.0
            elif user_id == "user_003":
                accuracy_probability = 0.60
                base_response_time = 7.0
            elif user_id == "user_004":
                accuracy_probability = 0.45
                base_response_time = 9.0
            else:
                accuracy_probability = 0.30
                base_response_time = 12.0

            # Simulate fatigue by gradually increasing response time.
            fatigue_multiplier = 1 + (position / 20) * 0.8

            response_time = max(
                1.0,
                random.gauss(
                    base_response_time * fatigue_multiplier,
                    0.8,
                ),
            )

            is_correct = (
                random.random() < accuracy_probability
            )

            if is_correct:
                selected_option = question["correct_option"]
            else:
                incorrect_options = [
                    option
                    for option in range(4)
                    if option != question["correct_option"]
                ]
                selected_option = random.choice(incorrect_options)

            submitted_at = shown_at + timedelta(
                seconds=response_time
            )

            attempts.append(
                {
                    "user_id": user_id,
                    "quiz_id": question["chapter_id"],
                    "question_id": question["question_id"],
                    "exam_id": question["exam_id"],
                    "subject_id": question["subject_id"],
                    "chapter_id": question["chapter_id"],
                    "question_shown_at": shown_at,
                    "answer_submitted_at": submitted_at,
                    "response_duration_seconds": round(
                        response_time,
                        2,
                    ),
                    "selected_option": selected_option,
                    "is_correct": is_correct,
                }
            )

    if attempts:
        db.attempts.insert_many(attempts)

    print(
        f"Generated {len(attempts)} analytics demo attempts "
        f"for {len(users)} users."
    )


if __name__ == "__main__":
    generate_demo_attempts()