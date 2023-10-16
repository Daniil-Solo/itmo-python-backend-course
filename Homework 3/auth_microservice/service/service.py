from auth_microservice.service.utils import hash_password
from protos.auth_pb2_grpc import AuthServiceServicer
from protos.auth_pb2 import (
    LoginRequest, LoginResponse,
    LogoutRequest, LogoutResponse,
    UserRequest, UserResponse
)
from auth_microservice.service.repository import (
    SessionRepositoryContextManager, BothRepositoryContextManager
)


class AuthServicer(AuthServiceServicer):
    async def login(self, request: LoginRequest, context) -> LoginResponse:
        async with BothRepositoryContextManager() as repos:
            session_repo, student_repo = repos
            student = await student_repo.get_one_by_login_and_hash_password(
                login=request.login, hashed_password=hash_password(request.password)
            )
            if student is None:
                return LoginResponse(session_id=None, timestamp=None)
            session = await session_repo.add_one(student.id)
        return LoginResponse(session_id=str(session.id), timestamp=session.expire_timestamp)

    async def logout(self, request: LogoutRequest, context) -> LogoutResponse:
        async with SessionRepositoryContextManager() as repo:
            await repo.update(session_id=request.session_id, is_active=False)
        return LogoutResponse()

    async def get_user(self, request: UserRequest, context) -> UserResponse:
        async with SessionRepositoryContextManager() as repo:
            session = await repo.get_one(session_id=request.session_id)
            if session is None:
                return UserResponse(user_id=None)
        return UserResponse(user_id=str(session.student_id))
