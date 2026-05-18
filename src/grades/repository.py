from src.commons.postgres import Postgres
from src.grades.model import Grade
from src.commons.unit_of_work import UnitOfWork


class GradeRepository:
    def __init__(self, db: Postgres, uow: UnitOfWork):
        self.db = db
        self.uow = uow
    
    async def save(self, grade: Grade) -> Grade:
        query = "INSERT INTO grades (student_id, \"date\", grade) VALUES ($1, $2, $3) RETURNING id"

        if self.uow.current_connection:
            conn = self.uow.current_connection
            grade_id = await conn.fetchval(query, grade.student.id, grade.date, grade.grade)
            grade.id = grade_id

            return grade
        else:
            async with self.db.connection() as conn:
                grade_id = await conn.fetchval(query, grade.student.id, grade.date, grade.grade)
                grade.id = grade_id

                return grade