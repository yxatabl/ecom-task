from src.students.model import Student, StudentStats
from src.students.repository import StudentRepository


class StudentService:
    def __init__(self, repository: StudentRepository):
        self.repository = repository

    async def save_student(self, student: Student) -> Student:
        student = await self.repository.save(student)
        return student
    
    async def get_students_stats_with_condition(self, grade: int, limit: int, higher: bool = True) -> list[StudentStats]:
        result = await self.repository.get_with_condition(grade, limit, higher)
        return result