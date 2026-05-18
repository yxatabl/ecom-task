from src.grades.model import Grade
from src.grades.repository import GradeRepository
from src.commons.unit_of_work import UnitOfWork
from src.students.repository import StudentRepository


class GradeService:
    def __init__(self, repository: GradeRepository, student_repository: StudentRepository, unit_of_work: UnitOfWork):
        self.repository = repository
        self.student_repository = student_repository
        self.uow = unit_of_work
    
    async def save_grades(self, grades: list[Grade]) -> tuple[int, int]:
        saved_grades = []
        student_ids = set()

        async with self.uow.transaction():
            for grade in grades:
                student = await self.student_repository.save(grade.student)
                grade.student = student
                student_ids.add(student.id)

                saved_grade = await self.repository.save(grade)
                saved_grades.append(saved_grade)
        
        return len(saved_grades), len(student_ids)