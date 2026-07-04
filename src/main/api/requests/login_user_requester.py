import requests
from requests import Response
from src.main.api.configs.config import Config
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.requests.requester import Requester


class LoginUserRequester(Requester):
    def post(self, login_user_request: LoginUserRequest) -> LoginUserResponse | Response:
        response = requests.post(
            url=f"{Config.fetch('backendUrl')}/auth/token/login",
            json=login_user_request.model_dump(),
            headers=self.request_spec,
        )
        self.response_spec(response)
        return LoginUserResponse(**response.json())
