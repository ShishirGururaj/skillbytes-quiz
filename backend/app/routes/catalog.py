from fastapi import APIRouter, Depends

from app.database import get_database


router = APIRouter(tags=["Catalog"])


@router.get("/api/exams")
def get_exams(database=Depends(get_database)):
    return list(
        database.exams.find(
            {},
            {"_id": 0},
        )
    )


@router.get("/api/exams/{exam_id}/subjects")
def get_subjects(
    exam_id: str,
    database=Depends(get_database),
):
    return list(
        database.subjects.find(
            {"exam_id": exam_id},
            {"_id": 0},
        )
    )


@router.get("/api/subjects/{subject_id}/chapters")
def get_chapters(
    subject_id: str,
    database=Depends(get_database),
):
    return list(
        database.chapters.find(
            {"subject_id": subject_id},
            {"_id": 0},
        )
    )