from functools import lru_cache

from fastapi import Depends

from src.commons.postgres import database

from src.dependecies import get_uow

from src.grades.parser import GradesParser
from src.grades.repository import GradeRepository
from src.grades.service import GradeService

from src.commons.unit_of_work import UnitOfWork

from src.students.dependecies import get_student_repository
from src.students.repository import StudentRepository


@lru_cache
def get_csv_parser() -> GradesParser:
    return GradesParser()

@lru_cache
def get_grades_repository(uow: UnitOfWork = Depends(get_uow)) -> GradeRepository:
    return GradeRepository(database, uow)

@lru_cache
def get_grades_service(
    uow: UnitOfWork = Depends(get_uow),
    repository: GradeRepository = Depends(get_grades_repository),
    student_repository: StudentRepository = Depends(get_student_repository)
) -> GradeService:
    return GradeService(repository, student_repository, uow)