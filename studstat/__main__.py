import argparse
import sys

from tabulate import tabulate

from studstat.parsers import CSVParser
from studstat.report import ReportMaker, StudentsTableFileMissing

report_maker = ReportMaker(CSVParser())


def __median_coffee(args: argparse.Namespace):
    try:
        res_table = report_maker.median_coffee_report(*args.files)
        print(tabulate(res_table.rows, res_table.headers, tablefmt="grid"))
    except StudentsTableFileMissing as e:
        print(f"ERROR: file not exists {e.filepath}", file=sys.stderr)


def main():
    report_handlers = {"median-coffee": __median_coffee}

    parser = argparse.ArgumentParser(
        description="Generate reports from exam preparation data"
    )
    parser.add_argument(
        "--files", nargs="+", required=True, help="List of CSV files with student data"
    )
    parser.add_argument(
        "--report",
        required=True,
        choices=list(report_handlers.keys()),
        help="Report type",
    )

    args = parser.parse_args()

    report_handlers[args.report](args)


if __name__ == "__main__":
    main()
