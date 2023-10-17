from fastapi import APIRouter, Depends, Body
from api_gateway.time_checking.schemas import CourseList, OperationResult
from api_gateway.time_checking.dependencies import get_time_checking_service
from api_gateway.time_checking.service import TimeCheckingService


router = APIRouter(tags=["Проверка курсов на пересечение"])


@router.post(
    "/",
    response_model=OperationResult,
    description="Проверяет, есть ли пересечение курсов по времени занятий"
)
async def check_time_for_courses(
    courses: CourseList = Body(),
    time_checking_service: TimeCheckingService = Depends(get_time_checking_service)
) -> OperationResult:
    """
    Проверяет курсы
    :param courses: курсы
    :param time_checking_service: сервис для проверки курсов
    :return: результат операции
    """
    is_successful = await time_checking_service.check(courses)
    if is_successful:
        return OperationResult(is_successful=True, message="Курсы не пересекаются")
    else:
        return OperationResult(is_successful=False, message="К сожалению, курсы пересекаются")
