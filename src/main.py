from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.commons.postgres import database
from src.grades.controller import router as grades_router
from src.students.controller import router as students_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
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

app.include_router(grades_router)
app.include_router(students_router)