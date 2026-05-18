from fastapi import APIRouter, status, UploadFile, File, HTTPException
import csv
from src import model
import io
from pydantic import ValidationError
from parser import parse_file

router = APIRouter()

@router.post(
    '/upload-grades',
    status_code=status.HTTP_201_CREATED,
    tags=["grades"],
    summary="Загрузка оценок из CSV",
    description="Файл должен быть в формате 01.01.1970;<номер группы>;<ФИО>;<оценка>\nПервая строка - заголовок\nРазделитель - только ;",
    responses={
        201: {
            "description": "Успешная загрузка",
            "content": {
                "application/json": {
                    "example": {
                        "status": "ok",
                        "records_loaded": 30,
                        "students": 22
                    }
                }
            }
        },
        400: {"description": "Неверный формат файла или данных"},
        422: {"description": "Ошибка валидации данных"},
    }
)
async def upload_grades(
    file: UploadFile = File(
        ...,
        description="CSV файл с оценками",
        examples=["grades.csv"]
    )
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Разрешены только csv файлы")
    
    data = await file.read()
    grades_list = parse_file(data)
    
    if not grades_list:
        raise HTTPException(status_code=400, detail="Файл пустой или неверного формата")

    try:
        students, grades = await model.save_grades(grades_list)
    except ValidationError as err:
        raise HTTPException(status_code=422, detail=f"Ошибки валидации: {[e['msg'] for e in err.errors()]}")
    except ValueError as err:
        raise HTTPException(status_code=422, detail=f"Ошибка валидации: {str(err)}")

    return {
        "status": "ok",
        "records_loaded": int(grades),
        "students": int(students)
    }

@router.get(
    '/students/more-than-3-twos',
    tags=["students"],
    summary="Студенты с более чем 3 двойками",
    responses={
        200: {
            "description": "Список студентов",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "full_name": "Иванов Иван",
                            "count_twos": 7
                        }
                    ]
                }
            }
        }
    }    
)
async def more_than_three_twos():
    result = await model.get_students_with_condition(grade=2, limit=3)
    
    return [{
        "full_name": el[0],
        "count_twos": el[1]
    } for el in result]

@router.get(
    '/students/less-than-5-twos',
    tags=["students"],
    summary="Студенты с менее чем 5 двойками",
    responses={
        200: {
            "description": "Список студентов",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "full_name": "Петров Петр",
                            "count_twos": 2
                        }
                    ]
                }
            }
        }
    }  
)
async def less_than_five_twos():
    result = await model.get_students_with_condition(grade=2, limit=5, higher=False)

    return [{
        "full_name": el[0],
        "count_twos": el[1]
    } for el in result]