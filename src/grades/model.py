from datetime import date

from pydantic import BaseModel

from src.students.model import Student


class Grade(BaseModel):
    id: int | None = None
    student: Student
    grade: int
    date: date