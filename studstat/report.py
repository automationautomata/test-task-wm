import statistics
from dataclasses import dataclass
from typing import Iterable, Literal, Protocol

from studstat.models import StudentsTable

ReportType = Literal["median-coffee"]


class StudentsTableFileMissing(Exception):
    def __init__(self, filepath: str, *args):
        super().__init__(*args)
        self.filepath = filepath


class PasrsedFileNotExists(Exception):
    """Ошибка, которую поднимает парсер, если файла не существует"""


class ParserProtocol(Protocol):
    def parse(self, path: str) -> StudentsTable: ...


@dataclass
class ResultTable:
    headers: list[str]
    rows: list[Iterable]


class ReportMaker:
    def __init__(self, file_parser: ParserProtocol):
        self.file_parser = file_parser

    def median_coffee_report(self, *paths: str) -> ResultTable:
        students = self._files_to_one_table(*paths)

        medians = []
        for name, rows in students:
            median = statistics.median(row.coffee_spent for row in rows)
            medians.append([name, median])

        medians.sort(key=lambda x: x[1], reverse=True)

        return ResultTable(headers=["name", "median_coffee"], rows=medians)

    def _files_to_one_table(self, *paths: str) -> StudentsTable:
        students = StudentsTable()

        for path in paths:
            try:
                students.update(self.file_parser.parse(path))
            except PasrsedFileNotExists as e:
                raise StudentsTableFileMissing(path) from e
        return students
