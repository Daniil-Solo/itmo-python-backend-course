from typing import Optional
from fastapi import APIRouter, Query, Depends, Path, Body, Header, status
from fastapi.responses import JSONResponse
from courses.dependencies import get_course_service, get_choice_service
from courses.services import CourseService, StudentChoiceService
from courses.constants import Implementer, Role
from courses.schemas import CourseShort, CourseFull, SemesterPlanCreate, SemesterPlan, OperationResult
course_router = APIRouter()
choice_router = APIRouter()


@course_router.get(
    "/",
    response_model=list[CourseShort],
    description="Возвращает курсы по фильтрам"
)
async def get_courses(
        implementer: Implementer = Query(None),
        role: Role = Query(None),
        search: Optional[str] = Query(None),
        course_service: CourseService = Depends(get_course_service)
) -> list[CourseShort]:
    """
    Возвращает курсы по фильтрам
    :param implementer: реализатор курса (ИПКН, ПИШ, ВШ ЦК)
    :param role: для какой роли в проекте будет полезен курс (Data Engineer, ML Engineer, Data Analyst и AI Architect)
    :param search: часть названия курса
    :param course_service: сервис для работы с курсами
    :return: список курсов
    """
    return await course_service.get_courses(implementer, role, search)


@course_router.get(
    "/{course_id}/",
    response_model=CourseFull,
    description="Возвращает подробную информацию о курсе по переданному идентификатору"
)
async def get_course_info(
        course_id: int = Path(),
        course_service: CourseService = Depends(get_course_service)
) -> CourseFull:
    """
    Возвращает подробную информацию о курсе по переданному идентификатору
    :param course_id: идентификатор курса
    :param course_service: сервис для работы с курсами
    :return: подробная информация о курсе
    """
    return await course_service.get_course_info(course_id)


@choice_router.post(
    "/",
    response_model=SemesterPlan,
    description="Создает для студента план изучения дисциплин",
    status_code=status.HTTP_201_CREATED
)
async def create_semester_plan(
        student_id: int = Header(),
        semester_plan_create: SemesterPlanCreate = Body(),
        choice_service: StudentChoiceService = Depends(get_choice_service)
) -> SemesterPlan:
    """
    Создает для студента план изучения дисциплин
    :param student_id: идентификатор студента (в дальнейшем следует использовать авторизационный токен)
    :param semester_plan_create: содержит нагрузку для семестра (количество дисциплин)
    :param choice_service: сервис для работы с выбором курсов
    :return: план изучения дисциплин
    """
    return await choice_service.create_plan(student_id, semester_plan_create)


@choice_router.get(
    "/",
    response_model=SemesterPlan,
    description="Возвращает план изучения дисциплин для студента"
)
async def get_semester_plan(
        student_id: int = Header(),
        choice_service: StudentChoiceService = Depends(get_choice_service)
) -> SemesterPlan:
    """
    Возвращает план изучения дисциплин для студента
    :param student_id: идентификатор студента (в дальнейшем следует использовать авторизационный токен)
    :param choice_service: сервис для работы с выбором курсов
    :return: план изучения дисциплин
    """
    return await choice_service.get_plan(student_id)


@choice_router.post(
    "/courses/{course_id}/",
    response_model=OperationResult,
    description="Добавляет курс в план для изучения дисциплин",
    status_code=status.HTTP_201_CREATED
)
async def add_course(
        student_id: int = Header(),
        course_id: int = Path(),
        choice_service: StudentChoiceService = Depends(get_choice_service)
):
    """
    Добавляет курс в план для изучения дисциплин
    :param student_id: идентификатор студента (в дальнейшем следует использовать авторизационный токен)
    :param course_id: идентификатор курса
    :param choice_service: сервис для работы с выбором курсов
    :return: результат операции
    """
    operation = await choice_service.add_course(student_id, course_id)
    return JSONResponse(
        content=operation.model_dump(),
        status_code=status.HTTP_201_CREATED if operation.is_successful else status.HTTP_200_OK
    )


@choice_router.post(
    "/confirm/",
    response_model=OperationResult,
    description="Подтверждает план изучения дисциплин"
)
async def confirm_plan(
        student_id: int = Header(),
        choice_service: StudentChoiceService = Depends(get_choice_service)
) -> OperationResult:
    """
    Подтверждает план изучения дисциплин
    :param student_id: идентификатор студента (в дальнейшем следует использовать авторизационный токен)
    :param choice_service: сервис для работы с выбором курсов
    :return: результат операции
    """
    return await choice_service.confirm_plan(student_id)


@choice_router.delete(
    "/courses/{course_id}/",
    response_model=OperationResult,
    description="Удаляет курс из плана для изучения дисциплин"
)
async def remove_course(
        student_id: int = Header(),
        course_id: int = Path(),
        choice_service: StudentChoiceService = Depends(get_choice_service)
) -> OperationResult:
    """
    Удаляет курс из плана для изучения дисциплин
    :param student_id: идентификатор студента (в дальнейшем следует использовать авторизационный токен)
    :param course_id: идентификатор курса
    :param choice_service: сервис для работы с выбором курсов
    :return: результат операции
    """
    return await choice_service.remove_course(student_id, course_id)
