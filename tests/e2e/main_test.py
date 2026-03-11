import sys
import pytest

from studstat.__main__ import main


def test_cli_median_coffee_e2e(tmp_path, capsys, monkeypatch):
    content = "\n".join(
        (
            "student,date,coffee_spent,sleep_hours,study_hours,mood,exam",
            "Иван Кузнецов,2024-06-11,720,2.0,18,не выжил,Программирование",
            "Иван Кузнецов,2024-06-12,780,1.5,20,труп,Программирование",
            "Иван Кузнецов,2024-06-13,820,1.0,22,легенда,Программирование",
            "Иван Кузнецов,2024-06-06,650,2.5,16,зомби,Физика",
            "Иван Кузнецов,2024-06-07,700,2.0,18,не выжил,Физика",
            "Иван Кузнецов,2024-06-08,750,1.5,20,труп,Физика",
            "Иван Кузнецов,2024-06-01,600,3.0,15,зомби,Математика",
            "Иван Кузнецов,2024-06-02,650,2.5,17,зомби,Математика",
            "Иван Кузнецов,2024-06-03,700,2.0,18,не выжил,Математика",
        )
    )

    file = tmp_path / "data.csv"
    file.write_text(content)

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "prog",
            "--files",
            str(file),
            "--report",
            "median-coffee",
        ],
    )

    main()

    captured = capsys.readouterr()

    assert "Иван Кузнецов" in captured.out
    assert "median_coffee" in captured.out

    assert "700" in captured.out


def test_cli_file_not_exists(capsys, monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "prog",
            "--files",
            "missing.csv",
            "--report",
            "median-coffee",
        ],
    )

    main()

    captured = capsys.readouterr()

    assert "ERROR: file not exists" in captured.err
