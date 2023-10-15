from typing import Optional
from fastapi import APIRouter, Query, Depends, Path
from api_gateway.courses.schemas import CourseShort, CourseFull
from api_gateway.courses.constants import Role, Implementer
from api_gateway.courses.dependencies import get_course_service
from api_gateway.courses.service import CourseService


router = APIRouter(tags=["Курсы"])


@router.get(
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


@router.get(
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
