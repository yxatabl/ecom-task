from datetime import date

from src.commons.postgres import database

from src.grades.dependencies import get_uow
from src.grades.model import Grade
from src.grades.repository import GradeRepository

from src.students.model import Student
from src.students.repository import StudentRepository
from src.students.service import StudentService



async def test_get_students_stats_higher_condition():
    uow = get_uow()
    student_repo = StudentRepository(database, uow)
    grade_repo = GradeRepository(database, uow)
    student_service = StudentService(student_repo)

    s1 = await student_repo.save(Student(fullname="Студент Один", group="101"))
    s2 = await student_repo.save(Student(fullname="Студент Два", group="101"))

    await grade_repo.save(Grade(student=s1, grade=2, date=date.today()))
    await grade_repo.save(Grade(student=s1, grade=2, date=date.today()))
    await grade_repo.save(Grade(student=s2, grade=2, date=date.today()))

    stats = await student_service.get_students_stats_with_condition(grade=2, limit=1, higher=True)

    assert len(stats) == 1
    assert stats[0].fullname == "Студент Один"
    assert stats[0].grades_num == 2


async def test_get_students_stats_lower_condition():
    uow = get_uow()
    student_repo = StudentRepository(database, uow)
    grade_repo = GradeRepository(database, uow)
    student_service = StudentService(student_repo)

    s1 = await student_repo.save(Student(fullname="Студент А", group="102"))
    s2 = await student_repo.save(Student(fullname="Студент Б", group="102"))

    await grade_repo.save(Grade(student=s1, grade=2, date=date.today()))
    await grade_repo.save(Grade(student=s2, grade=2, date=date.today()))
    await grade_repo.save(Grade(student=s2, grade=2, date=date.today()))
    await grade_repo.save(Grade(student=s2, grade=2, date=date.today()))

    stats = await student_service.get_students_stats_with_condition(grade=2, limit=2, higher=False)

    assert len(stats) == 1
    assert stats[0].fullname == "Студент А"
    assert stats[0].grades_num == 1