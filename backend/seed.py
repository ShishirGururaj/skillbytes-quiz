import random
from datetime import datetime, timezone

from pymongo import MongoClient

from app.config import settings
from app.database import create_indexes


random.seed(42)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def build_users() -> list[dict]:
    return [
        {
            "user_id": f"user_{index:03d}",
            "name": f"Student {index:03d}",
            "email": f"student{index:03d}@example.com",
            "created_at": utc_now(),
        }
        for index in range(1, 51)
    ]


def build_exams() -> list[dict]:
    exam_names = [
        "Python Fundamentals",
        "Web Development",
        "Software Engineering",
    ]

    return [
        {
            "exam_id": f"exam_{index:03d}",
            "name": name,
            "description": f"Assessment covering {name.lower()}.",
        }
        for index, name in enumerate(exam_names, start=1)
    ]


def build_subjects() -> list[dict]:
    subject_names = [
        "Python",
        "Data Structures",
        "Algorithms",
        "HTML & CSS",
        "JavaScript",
        "React",
        "Backend Development",
        "Databases",
        "APIs",
        "Software Engineering",
    ]

    subjects = []

    for index, name in enumerate(subject_names, start=1):
        exam_id = f"exam_{((index - 1) % 3) + 1:03d}"

        subjects.append(
            {
                "subject_id": f"subject_{index:03d}",
                "exam_id": exam_id,
                "name": name,
                "description": f"Questions related to {name}.",
            }
        )

    return subjects


def build_chapters(subjects: list[dict]) -> list[dict]:
    chapters = []

    chapter_number = 1

    for subject in subjects:
        for chapter_offset in range(1, 4):
            chapters.append(
                {
                    "chapter_id": f"chapter_{chapter_number:03d}",
                    "subject_id": subject["subject_id"],
                    "exam_id": subject["exam_id"],
                    "name": (
                        f"{subject['name']} "
                        f"Chapter {chapter_offset}"
                    ),
                }
            )
            chapter_number += 1

    return chapters


def build_questions(chapters: list[dict]) -> list[dict]:
    questions = []

    option_templates = [
        [
            "Option A",
            "Option B",
            "Option C",
            "Option D",
        ],
        [
            "Choice 1",
            "Choice 2",
            "Choice 3",
            "Choice 4",
        ],
    ]

    for index in range(1, 501):
        chapter = chapters[(index - 1) % len(chapters)]
        options = option_templates[index % len(option_templates)]

        correct_index = (index * 7) % 4

        questions.append(
            {
                "question_id": f"question_{index:04d}",
                "exam_id": chapter["exam_id"],
                "subject_id": chapter["subject_id"],
                "chapter_id": chapter["chapter_id"],
                "text": (
                    f"Question {index}: "
                    f"What is an important concept in "
                    f"{chapter['name']}?"
                ),
                "options": options,
                "correct_option": correct_index,
                "difficulty": ["easy", "medium", "hard"][index % 3],
            }
        )

    return questions


def seed() -> None:
    client = MongoClient(settings.mongodb_url)
    database = client[settings.mongodb_database]

    collections = [
        "users",
        "exams",
        "subjects",
        "chapters",
        "questions",
        "attempts",
    ]

    for collection_name in collections:
        database[collection_name].delete_many({})

    users = build_users()
    exams = build_exams()
    subjects = build_subjects()
    chapters = build_chapters(subjects)
    questions = build_questions(chapters)

    database.users.insert_many(users)
    database.exams.insert_many(exams)
    database.subjects.insert_many(subjects)
    database.chapters.insert_many(chapters)
    database.questions.insert_many(questions)

    create_indexes()

    print("Seed completed successfully.")
    print(f"Users:     {len(users)}")
    print(f"Exams:     {len(exams)}")
    print(f"Subjects:  {len(subjects)}")
    print(f"Chapters:  {len(chapters)}")
    print(f"Questions: {len(questions)}")

    client.close()


if __name__ == "__main__":
    seed()