from pydantic import BaseModel


class Student(BaseModel):
    id: int | None = None
    fullname: str
    group: str


class StudentStats(BaseModel):
    fullname: str
    grades_num: int