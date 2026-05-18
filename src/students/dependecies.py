from fastapi import Depends

from functools import lru_cache

from src.commons.unit_of_work import UnitOfWork
from src.dependecies import get_uow
from src.students.repository import StudentRepository
from src.commons.postgres import database
from src.students.service import StudentService



@lru_cache
def get_student_repository(uow: UnitOfWork = Depends(get_uow)) -> StudentRepository:
    return StudentRepository(database, uow)

@lru_cache
def get_student_service(repository: StudentRepository = Depends(get_student_repository)) -> StudentService:
    return StudentService(repository)