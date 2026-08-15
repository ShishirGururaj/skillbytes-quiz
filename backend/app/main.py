from fastapi import FastAPI

from app.routes.catalog import router as catalog_router
from app.routes.quiz import router as quiz_router

app = FastAPI(
    title="SkillBytes Quiz API",
    version="1.0.0",
)

app.include_router(catalog_router)
app.include_router(quiz_router)

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}