import pytest
from datetime import date
from unittest.mock import Mock

from studstat.report import ReportMaker, PasrsedFileNotExists, StudentsTableFileMissing
from studstat.models import StudentInfo, StudentsTable


@pytest.fixture
def student_info_factory():
    def _make(coffee: int):
        return StudentInfo(
            date=date(2024, 6, 1),
            coffee_spent=coffee,
            sleep_hours=7,
            study_hours=5,
            mood="ok",
            exam="math",
        )

    return _make


@pytest.fixture
def parser_mock():
    return Mock()


@pytest.fixture
def report_maker(parser_mock):
    return ReportMaker(parser_mock)


def test_median_coffee_single_file(report_maker, parser_mock, student_info_factory):
    table = StudentsTable(
        {
            "Влад": [
                student_info_factory(2),
                student_info_factory(4),
                student_info_factory(6),
            ],
            "Маша": [
                student_info_factory(1),
                student_info_factory(3),
                student_info_factory(5),
            ],
        }
    )

    parser_mock.parse.return_value = table

    result = report_maker.median_coffee_report("file.csv")

    assert result.headers == ["name", "median_coffee"]
    rows = dict(result.rows)

    assert rows["Влад"] == 4
    assert rows["Маша"] == 3

    parser_mock.parse.assert_called_once_with("file.csv")


def test_median_coffee_multiple_files(report_maker, parser_mock, student_info_factory):
    table1 = StudentsTable(
        {
            "Маша": [student_info_factory(2), student_info_factory(4)],
        }
    )

    table2 = StudentsTable(
        {
            "Маша": [student_info_factory(6)],
            "Влад": [
                student_info_factory(1),
                student_info_factory(3),
                student_info_factory(5),
            ],
        }
    )

    parser_mock.parse.side_effect = [table1, table2]

    result = report_maker.median_coffee_report("file1.csv", "file2.csv")

    rows = dict(result.rows)

    assert rows["Маша"] == 4
    assert rows["Влад"] == 3

    assert parser_mock.parse.call_count == 2


def test_rows_sorted_desc(report_maker, parser_mock, student_info_factory):
    table = StudentsTable(
        {
            "Маша": [
                student_info_factory(1),
                student_info_factory(1),
                student_info_factory(1),
            ],
            "Влад": [
                student_info_factory(5),
                student_info_factory(5),
                student_info_factory(5),
            ],
        }
    )

    parser_mock.parse.return_value = table

    result = report_maker.median_coffee_report("file.csv")

    assert result.rows[0][0] == "Влад"
    assert result.rows[1][0] == "Маша"


def test_file_not_exists(report_maker, parser_mock):
    parser_mock.parse.side_effect = PasrsedFileNotExists("missing.csv")

    with pytest.raises(StudentsTableFileMissing):
        report_maker.median_coffee_report("missing.csv")
