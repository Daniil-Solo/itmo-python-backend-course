import pytest
from fastapi.testclient import TestClient
from app import app


@pytest.fixture
def client():
    """
    Фикстура для получения клиента.
    Здесь неявно происходит проведение миграций и добавление всех данных для тестовой БД.
    Так как контекстный менеджер TestClient вызывает событие "startup", запускающее create_db.
    """
    with TestClient(app) as current_client:
        yield current_client


def test_get_courses_with_incorrect_filters(client):
    # Поиск по роли
    res = client.get(
        "/courses/?role=" + 'Роль которого не существует'
    )
    assert res.status_code == 422

    # Поиск по роли
    res = client.get(
        "/courses/?implementer=" + 'Реализатор которого не существует'
    )
    assert res.status_code == 422


def test_get_plan_with_incorrect_student_identification(client):
    # отсутствует заголовок с идентификатором студента
    res = client.get(
        "/semester_plan/"
    )
    assert res.status_code == 422

    # студента с таким id не существует
    res = client.get(
        "/semester_plan/",
        headers={
            'student-id': "120312"
        }
    )
    assert res.status_code == 404


def test_get_plan_with_right_student_identification(client):
    # создание плана
    res = client.post(
        "/semester_plan/",
        json={"semester_load": 3},
        headers={
            'student-id': "1"
        }
    )
    assert res.status_code == 201

    # получение созданного плана
    res = client.get(
        "/semester_plan/",
        headers={
            'student-id': "1"
        }
    )
    assert res.status_code == 200
    assert res.json()["semester_load"] == 3
    assert not res.json()["is_confirmed"]


def test_choice_courses_duplicate(client):
    # создание плана с нагрузкой 3
    res = client.post(
        "/semester_plan/",
        json={"semester_load": 3},
        headers={
            'student-id': "1"
        }
    )
    assert res.status_code == 201

    # Добавление курса с id=1
    res = client.post(
        "/semester_plan/courses/1/",
        headers={
            'student-id': "1"
        }
    )
    assert res.status_code == 201
    assert res.json()["is_successful"]

    # Добавление того же курса с id=1
    # должна быть ошибка, так как он уже выбран
    res = client.post(
        "/semester_plan/courses/1/",
        headers={
            'student-id': "1"
        }
    )
    assert res.status_code == 200
    assert not res.json()["is_successful"]


def test_choice_courses_remove(client):
    # создание плана с нагрузкой 3
    res = client.post(
        "/semester_plan/",
        json={"semester_load": 3},
        headers={
            'student-id': "1"
        }
    )
    assert res.status_code == 201

    # Добавление курса с id=1
    res = client.post(
        "/semester_plan/courses/1/",
        headers={
            'student-id': "1"
        }
    )

    # Удаление курса с id=1
    res = client.delete(
        "/semester_plan/courses/1/",
        headers={
            'student-id': "1"
        }
    )
    assert res.status_code == 200
    assert res.json()["is_successful"]


def test_choice_courses_limit(client):
    # создание плана с нагрузкой 2
    res = client.post(
        "/semester_plan/",
        json={"semester_load": 2},
        headers={
            'student-id': "1"
        }
    )
    assert res.status_code == 201

    # Добавление курса с id=1
    res = client.post(
        "/semester_plan/courses/1/",
        headers={
            'student-id': "1"
        }
    )
    # Добавление курса с id=2
    res = client.post(
        "/semester_plan/courses/2/",
        headers={
            'student-id': "1"
        }
    )
    assert res.status_code == 201
    assert res.json()["is_successful"]

    # Добавление курса с id=3
    # операция не должна завершиться успешно, так как лимит превышен
    res = client.post(
        "/semester_plan/courses/3/",
        headers={
            'student-id': "1"
        }
    )
    assert res.status_code == 200
    assert not res.json()["is_successful"]


def test_choice_courses_cross_lessons(client):
    # создание плана с нагрузкой 3
    res = client.post(
        "/semester_plan/",
        json={"semester_load": 3},
        headers={
            'student-id': "1"
        }
    )
    assert res.status_code == 201

    # Добавление курса с id=4
    res = client.post(
        "/semester_plan/courses/4/",
        headers={
            'student-id': "1"
        }
    )
    assert res.status_code == 201
    assert res.json()["is_successful"]

    # Добавление курса с id=11, который пересекается с уже добавленным
    # Должен завершится ошибкой
    res = client.post(
        "/semester_plan/courses/11/",
        headers={
            'student-id': "1"
        }
    )
    assert res.status_code == 200
    assert not res.json()["is_successful"]


def test_confirm_plan(client):
    # создание плана с нагрузкой 2
    res = client.post(
        "/semester_plan/",
        json={"semester_load": 2},
        headers={
            'student-id': "1"
        }
    )
    assert res.status_code == 201

    # Добавление курса с id=1
    res = client.post(
        "/semester_plan/courses/1/",
        headers={
            'student-id': "1"
        }
    )
    assert res.status_code == 201
    assert res.json()["is_successful"]

    # Попытка подтверждения выбора не должна пройти успешно
    # Так как набрано недостаточное количество дисциплин
    res = client.post(
        "/semester_plan/confirm/",
        headers={
            'student-id': "1"
        }
    )
    assert res.status_code == 200
    assert not res.json()["is_successful"]

    # Добавление курса с id=2
    res = client.post(
        "/semester_plan/courses/2/",
        headers={
            'student-id': "1"
        }
    )
    assert res.status_code == 201
    assert res.json()["is_successful"]

    # Подтверждение выбора
    res = client.post(
        "/semester_plan/confirm/",
        headers={
            'student-id': "1"
        }
    )
    assert res.status_code == 200
    assert res.json()["is_successful"]

    # Получение плана
    res = client.get(
        "/semester_plan/",
        headers={
            'student-id': "1"
        }
    )
    assert res.status_code == 200
    assert res.json()["is_confirmed"]

    # Изменение курса для подтвержденного плана запрещено
    res = client.post(
        "/semester_plan/courses/5/",
        headers={
            'student-id': "1"
        }
    )
    assert res.status_code == 200
    assert not res.json()["is_successful"]

    res = client.delete(
        "/semester_plan/courses/1/",
        headers={
            'student-id': "1"
        }
    )
    assert res.status_code == 200
    assert not res.json()["is_successful"]
