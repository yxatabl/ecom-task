from typing import Optional
import asyncpg
from src.commons.postgres import Postgres
from src.commons.unit_of_work import UnitOfWork
from src.students.model import Student, StudentStats


class StudentRepository:
    def __init__(self, db: Postgres, uow: UnitOfWork):
        self.db = db
        self.uow = uow

    def _get_connection(self) -> Optional[asyncpg.Connection]:
        return self.uow.current_connection

    async def save(self, student: Student) -> Student:
        query = """
            INSERT INTO students ("group", fullname)
            VALUES ($1, $2)
            ON CONFLICT ("group", fullname) DO UPDATE
            SET "group" = EXCLUDED."group"
            RETURNING id
        """
        
        tx_conn = self._get_connection()
        if tx_conn:
            student_id = await tx_conn.fetchval(query, student.group, student.fullname)
            student.id = student_id
            return student
        
        async with self.db.connection() as conn:
            student_id = await conn.fetchval(query, student.group, student.fullname)
            student.id = student_id
            return student
    
    async def get_by_id(self, student_id: int) -> Optional[Student]:
        query = 'SELECT id, fullname, "group" FROM students WHERE id = $1'
        
        tx_conn = self._get_connection()
        if tx_conn:
            row = await tx_conn.fetchrow(query, student_id)
        else:
            async with self.db.connection() as conn:
                row = await conn.fetchrow(query, student_id)

        if not row:
            return None

        return Student(id=row["id"], fullname=row["fullname"], group=row["group"])
    
    async def get_with_condition(self, grade: int, limit: int, higher: bool = True) -> list[StudentStats]:
        operator = '>' if higher else '<'

        query = f"""
            SELECT st.fullname, count(*) AS grades_num 
            FROM grades AS gr
            JOIN students AS st ON gr.student_id = st.id
            WHERE gr.grade = $1
            GROUP BY st.id, st.fullname
            HAVING count(*) {operator} $2
        """
        
        tx_conn = self._get_connection()
        if tx_conn:
            result = await tx_conn.fetch(query, grade, limit)
        else:
            async with self.db.connection() as conn:
                result = await conn.fetch(query, grade, limit)

        return [
            StudentStats(fullname=row["fullname"], grades_num=row["grades_num"]) 
            for row in result
        ]
