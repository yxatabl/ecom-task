import csv
import io

def parse_file(data: bytes) -> list[tuple[str, str, str, str]]:
    data_decoded = data.decode('utf-8')
    reader = csv.reader(io.StringIO(data_decoded), delimiter=';')
    next(reader, None)

    grades_list = []
    for row in reader:
        if len(row) >= 4:
            grades_list.append((row[0], row[1], row[2], row[3]))
    
    return grades_list