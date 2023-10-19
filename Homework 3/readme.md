## Домашнее задание №2

### О задании
1. Определить несколько микросервисов, которые будут выполнять разные функции. Например, микросервисы для обработки заказов, аутентификации, и управления пользователями или ML-модели
2. Для каждого микросервиса определить API, используя gRPC или HTTP, для взаимодействия между сервисами.
3. Реализовать функциональность каждого микросервиса. В целом достаточно одного главного сервиса к которому стучится клиент и 2-х вспомогательных сервисов
4. Покройте функционал тестами

### О решении
1. Архитектура системы для выбора дисциплин:
    - API Gateway для предоставления единого API и объединения других микросервисов
    - AuthMicroservice - микросервис аутентификации (только login, logout)
    - CourseMicroservice - микросервис информации о курсах
    - TimeCheckingMicroservice - микросервис проверки пересечения курсов по времени занятий — может обращаться к CourseMicroservice 
      
2. Клиент общается с API Gateway через HTTP. API Gateway обращается к остальными микросервисами через gRPC.
add_CheckTimeServiceServicer_to_server общается с CourseMicroservice через gRPC.
У AuthMicroservice и CourseMicroservice своя база данных, для простоты это SQLite. 
Переменные окружения для всех микросервисов для простоты находятся в одном env-файле.
3. Микросервисы реализованы (о запуске микросервисов ниже)
4. Добавлены тесты (о запуске тестов ниже)
    
### Установка зависимостей
```cmd
pip install poetry
poetry install
```

### Переменные окружения
Для запуска приложение использует переменные из файла .env.example 
```
MODE=DEV
COURSE_ADDRESS=localhost:5670
AUTH_ADDRESS=localhost:5671
TIME_CHECKING_ADDRESS=localhost:5672
COURSE_DB_FILEPATH=some_path\course_microservice\db.sqlite
AUTH_DB_FILEPATH=some_path\auth_microservice\db.sqlite
```

### Запуск приложения
__Запуск API Gateway:__
```cmd
cd ./"Homework 3"
poetry run uvicorn api_gateway.app:app --port 5000
```
__Запуск микросервиса для курсов:__
```cmd
cd ./"Homework 3"
poetry run python -m course_microservice.app
```
__Запуск микросервиса для аутентификации:__
```cmd
cd ./"Homework 3"
poetry run python -m auth_microservice.app
```
__Запуск микросервиса для проверки времени занятий:__
```cmd
cd ./"Homework 3"
poetry run python -m time_checking.app
```

### Линтеры
В проекте используется Pylint. Для запуска необходимо находиться в корне проекта, чтобы применилась конфигурация для pylint
```cmd
poetry run pylint ./"Homework 3"
```
В основном проверку не прошли файлы, которые были сгенерированы protoc, и файлы с производными классами

### Тестирование
Так как бизнес-логика была существенно упрощена, то и тестов не так много, только в юнит-тест в микросервисе для курсов
#### Запуск unit-тестов
```cmd
cd ./"Homework 3"
poetry run pytest course_microservice/tests/test_unittests.py
```
