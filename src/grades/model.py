from datetime import date

from pydantic import BaseModel, Field

from src.students.model import Student


class Grade(BaseModel):
    id: int | None = None
    student: Student
    grade: int = Field(ge=1, le=5)
    date: date