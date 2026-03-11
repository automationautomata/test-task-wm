# Тестовое задание


Перед запуском:
```console
$ poetry install 
```

Для запуска:
```console
$ poetry run studstat --files \<files> --report median-coffee
``` 

### Тесты
Перед запуском:
```console
$ poetry install --all-groups 
```

Для запуска тестов:
```console
$ poetry run pytest
```

![test_coverage](example_images/test_cov.png)

### Примеры

Запуск с отсутствующим файлом:
![run_without_file_example](example_images/without_file.png)

Запуск с отсутствующим типом отчета:
![run_with_invalid_report](example_images/invalid_report.png)

Запуск для всех:\
![run_all_example](example_images/run_all.png)

Запуск для programming.csv:
![run_prog_example](example_images/run_prog.png)

