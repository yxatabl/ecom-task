import csv
from datetime import datetime
from io import StringIO

from src.grades.model import Grade
from src.students.model import Student


class GradesParser:
    def parse(self, file_bytes: bytes) -> list[Grade]:
        csv_text = file_bytes.decode('utf-8-sig')
        csv_buffer = StringIO(csv_text)
        reader = csv.DictReader(csv_buffer, delimiter=';')

        grades = []
        for row in reader:
            try:
                grade_date = datetime.strptime(row['Дата'], '%d.%m.%Y').date()

                student = Student(group=row['Номер группы'], fullname=row['ФИО'])
                
                grade = Grade(
                    date=grade_date,
                    student=student,
                    grade=int(row['Оценка'])
                )
                grades.append(grade)

            except Exception:
                raise
        
        return grades