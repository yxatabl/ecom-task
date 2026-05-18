from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from src.grades.dependencies import get_csv_parser, get_grades_service
from src.grades.parser import GradesParser
from src.grades.service import GradeService

router = APIRouter()

@router.post('/upload-grades', status_code=201)
async def upload_grades(
    file: UploadFile = File(...),
    parser: GradesParser = Depends(get_csv_parser),
    service: GradeService = Depends(get_grades_service)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Разрешены только csv файлы")
    
    try:
        file_bytes = await file.read()
        grades = parser.parse(file_bytes)

        grades_count, students_count = await service.save_grades(grades)

        return {
            "status": "ok",
            "records_loaded": grades_count,
            "students": students_count
        }
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))