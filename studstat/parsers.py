import csv
from datetime import datetime

from studstat.models import StudentInfo, StudentsTable
from studstat.report import PasrsedFileNotExists


class CSVParser:
    def parse(self, path: str) -> StudentsTable:
        try:
            table = {}

            with open(path, mode="r", newline="") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    info = StudentInfo(
                        date=datetime.strptime(row["date"], "%Y-%m-%d").date(),
                        coffee_spent=int(row["coffee_spent"]),
                        sleep_hours=float(row["sleep_hours"]),
                        study_hours=int(row["study_hours"]),
                        mood=row["mood"],
                        exam=row["exam"],
                    )

                    name = row["student"]
                    if name not in table:
                        table[name] = []

                    table[name].append(info)

            return StudentsTable(table)

        except FileNotFoundError as e:
            raise PasrsedFileNotExists(path) from e
