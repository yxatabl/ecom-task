from typing import Any

from pydantic import BaseModel, field_validator
from datetime import date


class Student(BaseModel):
    full_name: str
    group: str


class Grade(BaseModel):
    date: date
    student_id: int
    grade: int

    @field_validator('grade')
    @classmethod
    def validate_grade(cls, v: Any):
        if v < 2 or v > 5:
            raise ValueError("Оценка должна быть от 1 до 5")
        return v