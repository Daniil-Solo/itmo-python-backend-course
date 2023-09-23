## Домашнее задание №1

### О задании
1. Создать “Hello world” на понравившемся фреймворке
2. Создать несколько entry point: с path параметром, query параметром и request body
3. Настроить линтеры, форматтеры
4. Написать комментарии для всех функций и entry point
5. Выложить в репозиторий на гитхаб

### О решении
1. В качестве фреймворка был выбран FastAPI
2. Создано 3 эндпоинта, находящиеся в `router.py`, и Pydantic-модели в `schemas.py`
3. Добавлен линтер pylint и в его конфигурации отключена необходимость указания docstring для модуля
4. Для каждой созданной функции и моделей Pydantic указаны комментарии
5. Работа опубликована как Pull Request

### Установка зависимостей
```cmd
pip install poetry
poetry install
```

### Пример запуска приложения
```cmd
cd ./"Homework 1"
poetry run uvicorn app:app --port=5000
```

### Пример запуска линтера
Необходимо находиться в корне проекта, чтобы применилась конфигурация для pylint
```cmd
poetry run pylint ./"Homework 1"/app.py
poetry run pylint ./"Homework 1"/constants.py
poetry run pylint ./"Homework 1"/router.py
poetry run pylint ./"Homework 1"/schemas.py
```
Все файлы прошли проверку pylint на 10