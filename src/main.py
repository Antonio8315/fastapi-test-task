from fastapi import FastAPI
from src.core.config import settings
from src.api.v1 import category

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(category.router)

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok", "db_url": settings.DATABASE_URL}