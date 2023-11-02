## Домашнее задание №4

### О задании
1. Придумать сценарий с использованием очередей
2. Реализовать как минимум 1 продьюсер и 2-3 воркера Celery, которые будут обрабатывать задачи из разных очередей
3. При реализации использовать RabbitMQ и Celery

### О решении
1. Выполняемые операции:
   - Факториал: f(n) = n! (n <= 10)
   - Число Фибоначчи: fib(n) = fib(n-1) + fib(n-2) (n <= 50)
   - Ожидание n секунд (n <= 5)
2. Реализация:
    - API на FastAPI с возможностью созданием задач и запрашиванием результата
    - Celery-воркеры
3. В качестве брокера для Celery был использован RabbitMQ, в качестве бэкенда взят Redis

### Запуск
#### Сборка и запуск инфраструктуры
```cmd
cd "Homework 4"
mkdir rabbitmq_data
docker-compose up -d --build
```
#### Масштабирование воркеров
```cmd
docker-compose up --scale worker=3
```

#### Подключение к API
```cmd
http://127.0.0.1:8000/docs
```
#### Подключение к админ-панели RabbitMQ
```cmd
http://127.0.0.1:15672
```

### Линтеры
В проекте используется Pylint. Для запуска необходимо находиться в корне проекта, чтобы применилась конфигурация для pylint
```cmd
poetry run pylint "Homework 4"
```
Код проекта прошел проверку на 10