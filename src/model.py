from datetime import date, datetime

from src.schema import Student, Grade
from src.commons.postgres import database
from asyncpg import Connection

async def get_student_id(student: Student, conn: Connection) -> int:
    query = """
        INSERT INTO students ("group", fullname)
        VALUES ($1, $2)
        ON CONFLICT ("group", fullname) DO UPDATE
        SET "group" = EXCLUDED."group"
        RETURNING id
    """
    student_id = await conn.fetchval(query, student.group, student.full_name)
    return student_id

async def save_grade(grade: Grade, conn: Connection):
    query = "INSERT INTO grades (student_id, \"date\", grade) VALUES ($1, $2, $3)"

    await conn.execute(query, grade.student_id, grade.date, grade.grade)

async def save_grades(grades: list[tuple[date, str, str, int]]):
    async with database.pool.acquire() as conn:
        async with conn.transaction():
            for el in grades:
                student = Student(group=el[1], full_name=el[2])
                
                student_id = await get_student_id(student, conn)
                grade_date = datetime.strptime(el[0], '%d.%m.%Y').date()

                grade = Grade(date=grade_date, student_id=student_id, grade=int(el[3]))
                await save_grade(grade, conn)
            
            stats_query = "SELECT (SELECT count(*) FROM students), (SELECT count(*) FROM grades)"
            result = await conn.fetchrow(stats_query)
            return result[0], result[1]

async def get_students_with_condition(grade: int, limit: int, higher: bool = True) -> list[tuple[str, int]]:
    operator = '>' if higher else '<'

    query = f"""
        SELECT st.fullname, count(*) FROM grades AS gr
        JOIN students AS st ON gr.student_id = st.id
        WHERE gr.grade = $1
        GROUP BY st.id, st.fullname
        HAVING count(*) {operator} $2
    """

    async with database.pool.acquire() as conn:
        result = await conn.fetch(query, grade, limit)
    
    return result