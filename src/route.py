from fastapi import APIRouter, status, UploadFile, File, HTTPException
import csv
from src import model
import io
from pydantic import ValidationError

router = APIRouter()

@router.post('/upload-grades', status_code=status.HTTP_201_CREATED)
async def upload_grades(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Разрешены только csv файлы")
    
    data = await file.read()
    data_decoded = data.decode('utf-8')
    reader = csv.reader(io.StringIO(data_decoded), delimiter=';')
    next(reader, None)

    grades_list = []
    for row in reader:
        if len(row) >= 4:
            grades_list.append((row[0], row[1], row[2], row[3]))
    
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

@router.get('/students/more-than-3-twos')
async def more_than_three_twos():
    result = await model.get_students_with_condition(grade=2, limit=3)
    
    return [{
        "full_name": el[0],
        "count_twos": el[1]
    } for el in result]

@router.get('/students/less-than-5-twos')
async def less_than_five_twos():
    result = await model.get_students_with_condition(grade=2, limit=5, higher=False)

    return [{
        "full_name": el[0],
        "count_twos": el[1]
    } for el in result]