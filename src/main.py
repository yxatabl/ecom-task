from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.commons import migrate
from src.commons.postgres import database
from src.route import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    await migrate.apply_pending_migrations()
    yield
    await database.disconnect()

app = FastAPI(
    docs_url='/docs',
    title="Анализ оценок студентов",
    openapi_tags=[
        {'name': "grades", 'description': "Загрузка оценок"},
        {'name': "students", 'description': "Получение статистики по студентам"}
    ],
    lifespan=lifespan
)

app.include_router(router)