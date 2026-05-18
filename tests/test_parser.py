import pytest

from datetime import date

from src.grades.parser import GradesParser


def test_parser_success():
    parser = GradesParser()
    
    csv_content = (
        "Дата;Номер группы;ФИО;Оценка\n"
        "11.03.2025;101Б;Курочкин Антон Владимирович;4\n"
        "18.09.2024;102Б;Москвичев Андрей;3"
    ).encode('utf-8')

    result = parser.parse(csv_content)

    assert len(result) == 2

    assert result[0].date == date(2025, 3, 11)
    assert result[0].student.group == "101Б"
    assert result[0].student.fullname == "Курочкин Антон Владимирович"
    assert result[0].grade == 4

    assert result[1].date == date(2024, 9, 18)
    assert result[1].student.fullname == "Москвичев Андрей"
    assert result[1].grade == 3


def test_parser_with_bom_marker():
    parser = GradesParser()
    
    csv_content = "\ufeffДата;Номер группы;ФИО;Оценка\n01.02.2025;103М;Третьяков Максим;2".encode('utf-8')

    result = parser.parse(csv_content)
    
    assert len(result) == 1
    assert result[0].student.fullname == "Третьяков Максим"
    assert result[0].date == date(2025, 2, 1)


def test_parser_invalid_date_format_raises_error():
    parser = GradesParser()
    
    csv_content = (
        "Дата;Номер группы;ФИО;Оценка\n"
        "11-03-25;101Б;Курочкин Антон;4"
    ).encode('utf-8')

    with pytest.raises(ValueError):
        parser.parse(csv_content)


def test_parser_missing_column_raises_error():
    parser = GradesParser()
    
    csv_content = (
        "Дата;Номер группы;ФИО\n"
        "11.03.2025;101Б;Курочкин Антон Владимирович"
    ).encode('utf-8')

    with pytest.raises(KeyError):
        parser.parse(csv_content)


def test_parser_invalid_grade_type_raises_error():
    parser = GradesParser()
    
    csv_content = (
        "Дата;Номер группы;ФИО;Оценка\n"
        "11.03.2025;101Б;Курочкин Антон;хорошо"
    ).encode('utf-8')

    with pytest.raises(ValueError):
        parser.parse(csv_content)