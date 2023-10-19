from fastapi import APIRouter, Depends, Body, Cookie
from fastapi.responses import JSONResponse
from fastapi import status
from api_gateway.auth.schemas import Login, OperationResponse
from api_gateway.auth.dependencies import get_auth_service
from api_gateway.auth.service import AuthService
from api_gateway.auth.exceptions import LoginException

router = APIRouter(tags=["Аутентификация"])


@router.post(
    "/login/",
    description="Выполняет вход в систему",
    response_model=OperationResponse,
    status_code=status.HTTP_201_CREATED
)
async def login(
        login_data: Login = Body(),
        auth_service: AuthService = Depends(get_auth_service)
) -> JSONResponse:
    """
    Выполняет вход в систему
    :param login_data: данные для аутентификации
    :param auth_service: сервис для работы с аутентификацией
    :return: результат выполнения операции
    """
    try:
        session = await auth_service.login(login_data)
        response = JSONResponse(
            content=OperationResponse(message="Вход выполнен успешно").model_dump(),
            status_code=status.HTTP_201_CREATED
        )
        response.set_cookie("session_id", session.id, expires=str(session.expire_date))
        return response
    except LoginException:
        return JSONResponse(
            content=OperationResponse(message="Неверные данные для входа").model_dump(),
            status_code=status.HTTP_400_BAD_REQUEST
        )


@router.post(
    "/logout/",
    description="Выполняет выход из системы",
    response_model=OperationResponse,
    status_code=status.HTTP_200_OK
)
async def logout(
        session_id: str = Cookie(),
        auth_service: AuthService = Depends(get_auth_service)
) -> JSONResponse:
    """
    Выполняет выход из системы
    :param session_id: идентификатор сессии
    :param auth_service: сервис для работы с аутентификацией
    :return: результат выполнения операции
    """
    await auth_service.logout(session_id)
    response = JSONResponse(
        content=OperationResponse(message="Выход выполнен успешно").model_dump(),
        status_code=status.HTTP_200_OK
    )
    response.delete_cookie("session_id")
    return response
