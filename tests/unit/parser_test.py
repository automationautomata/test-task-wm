import pytest
from datetime import date

from studstat.parsers import CSVParser
from studstat.models import StudentInfo
from studstat.report import PasrsedFileNotExists


def test_parse_single_student(tmp_path):
    content = "\n".join(
        (
            "student,date,coffee_spent,sleep_hours,study_hours,mood,exam",
            "Алексей Смирнов,2024-06-01,450,4.5,12,норм,Математика",
            "Алексей Смирнов,2024-06-02,500,4.0,14,устал,Математика",
        )
    )

    file = tmp_path / "data.csv"
    file.write_text(content)

    parser = CSVParser()
    result = parser.parse(str(file))

    rows = result["Алексей Смирнов"]
    assert len(rows) == 2

    correct_rows = [
        StudentInfo(
            date=date(2024, 6, 1),
            coffee_spent=450,
            sleep_hours=4.5,
            study_hours=12,
            mood="норм",
            exam="Математика",
        ),
        StudentInfo(
            date=date(2024, 6, 2),
            coffee_spent=500,
            sleep_hours=4.0,
            study_hours=14,
            mood="устал",
            exam="Математика",
        ),
    ]
    assert rows == correct_rows


def test_parse_multiple_students(tmp_path):
    content = "\n".join(
        (
            "student,date,coffee_spent,sleep_hours,study_hours,mood,exam",
            "Иван Кузнецов,2024-06-03,700,2.0,18,не выжил,Математика",
            "Мария Соколова,2024-06-01,100,8.0,3,отл,Математика",
        )
    )

    file = tmp_path / "data.csv"
    file.write_text(content)

    parser = CSVParser()
    result = parser.parse(str(file))

    assert set(result.table.keys()) == {"Иван Кузнецов", "Мария Соколова"}
    assert len(result["Иван Кузнецов"]) == 1
    assert len(result["Мария Соколова"]) == 1


def test_parse_file_not_exists():
    parser = CSVParser()

    with pytest.raises(PasrsedFileNotExists):
        parser.parse("missing.csv")
