from fastapi import APIRouter, Query, Body, Path, HTTPException, status
from schemas import Course, Implementer, Role, CourseRequest, CourseRequestAnswer
from constants import COURSES


course_router = APIRouter()


@course_router.get("/",
                   response_model=list[Course],
                   description="Возвращает курсы по фильтрам")
def get_courses(implementer: Implementer or None = Query(None), role: Role or None = Query(None)):
    """
    Возвращает курсы по фильтрам. Список курсов задан константно
    :param implementer: реализатор курса (ИПКН, ПИШ, ВШ ЦК, Другое)
    :param role: для какой роли в проекте будет полезен курс
    (Data Engineer, Machine Learning Engineer, Data Analyst, AI Architect, AI Product Manager
    :return: список курсов
    """
    result = []
    for course in COURSES:
        is_passed = True
        if implementer is not None:
            is_passed = is_passed and implementer == course.implementer
        if role is not None:
            is_passed = is_passed and role in course.roles
        if is_passed:
            result.append(course)
    return result


@course_router.get("/{course_id}",
                   response_model=Course,
                   description="Возвращает курс по его id")
def get_course_by_id(course_id: int = Path()):
    """
    Возвращает курс по его id. Список курсов задан константно
    :param course_id:
    :return: информация о курсе
    """
    for course in COURSES:
        if course.id == course_id:
            return course
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Курс с идентификатором {course_id} не существует"
    )


@course_router.post("/requests",
                    response_model=CourseRequestAnswer,
                    description="Создает заявку на курс",
                    status_code=status.HTTP_201_CREATED)
def create_course_request(course_request: CourseRequest = Body()):
    """
    Создает заявку на курс. На данной момент реальной обработки не происходит
    :param course_request: заявка на курс
    :return: сообщение об успешном создании заявки
    """
    for course in COURSES:
        if course_request.course_id == course.id:
            selected_course = course
            break
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Курс с идентификатором {course_request.course_id} не существует"
        )
    return CourseRequestAnswer(
        message=f"Заявка на курс \"{selected_course.title}\" успешно создана! " +
                f"Ожидайте ответ по указанной электронной почте: {course_request.student_email}"
    )
