from dataclasses import dataclass, field
from datetime import date
from typing import Iterator, Self


@dataclass(frozen=True)
class StudentInfo:
    date: date
    coffee_spent: int
    sleep_hours: float
    study_hours: int
    mood: str
    exam: str


@dataclass
class StudentsTable:
    table: dict[str, list[StudentInfo]] = field(default_factory=dict)

    def __getitem__(self, name: str) -> list[StudentInfo]:
        rows = self.table.get(name, None)
        if rows is None:
            raise KeyError(f"Student with name '{name}' not found")
        return rows

    def add(self, name: str, *rows: StudentInfo):
        if name not in self.table:
            self.table[name] = []
        self.table[name].extend(rows)

    def update(self, other: Self):
        for name, rows in other:
            self.add(name, *rows)

    def __iter__(self) -> Iterator[tuple[str, list[StudentInfo]]]:
        return iter(self.table.items())
