from fastapi import FastAPI
from src.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok", "db_url": settings.DATABASE_URL}