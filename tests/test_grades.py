from datetime import datetime

from src.commons.postgres import database

from src.grades.dependencies import get_uow
from src.grades.model import Grade
from src.grades.repository import GradeRepository
from src.grades.service import GradeService

from src.students.model import Student
from src.students.repository import StudentRepository


async def test_import_grades_success():
    uow = get_uow()
    student_repo = StudentRepository(database, uow)
    grade_repo = GradeRepository(database, uow)
    service = GradeService(grade_repo, student_repo, uow)

    students = [
        Student(fullname="Владимир Петров", group="100А"),
        Student(fullname="Николай Петров", group="101Б"),
        Student(fullname="Николай Иванов", group="101В")
    ]

    grades = [
        Grade(student=students[0], grade=2, date=datetime.strptime("18.05.2025", '%d.%m.%Y').date()),
        Grade(student=students[1], grade=2, date=datetime.strptime("18.05.2025", '%d.%m.%Y').date()),
        Grade(student=students[2], grade=2, date=datetime.strptime("18.05.2025", '%d.%m.%Y').date()),
        Grade(student=students[0], grade=5, date=datetime.strptime("18.05.2025", '%d.%m.%Y').date()),
        Grade(student=students[0], grade=2, date=datetime.strptime("16.05.2025", '%d.%m.%Y').date())
    ]

    grades_added, students_added = await service.save_grades(grades)

    assert students_added == 3
    assert grades_added == 5