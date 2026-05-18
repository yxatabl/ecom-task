from fastapi import APIRouter, Depends

from src.students.dependecies import get_student_service
from src.students.service import StudentService

router = APIRouter(prefix="/students")

@router.get('/more-than-3-twos')
async def more_than_three_twos(student_service: StudentService = Depends(get_student_service)):
    result = await student_service.get_students_stats_with_condition(grade=2, limit=3)
    return [{
        "full_name": stat.fullname,
        "count_twos": stat.grades_num
    } for stat in result]

@router.get('/less-than-5-twos')
async def less_than_five_twos(student_service: StudentService = Depends(get_student_service)):
    result = await student_service.get_students_stats_with_condition(grade=2, limit=5, higher=False)
    return [{
        "full_name": stat.fullname,
        "count_twos": stat.grades_num
    } for stat in result]