from pymongo import ASCENDING, MongoClient
from pymongo.database import Database

from app.config import settings


client = MongoClient(settings.mongodb_url)
db: Database = client[settings.mongodb_database]


def get_database() -> Database:
    return db


def create_indexes() -> None:
    db.users.create_index([("user_id", ASCENDING)], unique=True)

    db.exams.create_index([("exam_id", ASCENDING)], unique=True)

    db.subjects.create_index([("subject_id", ASCENDING)], unique=True)
    db.subjects.create_index([("exam_id", ASCENDING)])

    db.chapters.create_index([("chapter_id", ASCENDING)], unique=True)
    db.chapters.create_index([("subject_id", ASCENDING)])

    db.questions.create_index([("question_id", ASCENDING)], unique=True)
    db.questions.create_index([("exam_id", ASCENDING), ("subject_id", ASCENDING)])
    db.questions.create_index([("chapter_id", ASCENDING)])