from api_gateway.auth.schemas import Login, Session
from protos.auth_pb2_grpc import AuthServiceStub
from protos.auth_pb2 import LoginRequest, LoginResponse, LogoutRequest
from auth_microservice.service.exceptions import LoginException
from datetime import datetime, timedelta


class AuthService:
    def __init__(self, stub: AuthServiceStub):
        self.stub = stub

    async def login(self, login_data: Login) -> Session:
        response: LoginResponse = await self.stub.login(
            LoginRequest(login=login_data.login, password=login_data.password)
        )
        if response.session_id == "" or response.timestamp == 0:
            raise LoginException
        return Session(id=response.session_id, expire_date=datetime.fromtimestamp(response.timestamp))

    async def logout(self, session_id: str) -> None:
        await self.stub.logout(
            LogoutRequest(session_id=session_id)
        )
