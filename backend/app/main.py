from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.catalog import router as catalog_router
from app.routes.quiz import router as quiz_router
from app.routes.analytics import router as analytics_router

app = FastAPI(
    title="SkillBytes Quiz API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(catalog_router)
app.include_router(quiz_router)
app.include_router(analytics_router)

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}