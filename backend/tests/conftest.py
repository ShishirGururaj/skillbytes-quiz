import pytest
from pymongo import MongoClient


@pytest.fixture
def database():
    client = MongoClient(
        "mongodb://localhost:27017"
    )

    database = client["skillbytes_quiz_test"]

    database.attempts.delete_many({})

    yield database

    database.attempts.delete_many({})
    client.drop_database("skillbytes_quiz_test")
    client.close()