from requests import Response
import requests

from src.main.api.models.login_user_response_model import LoginUserResponse
from src.main.api.models.login_user_request_model import LoginUserRequest
from src.main.api.requests.requester import Requester


class LoginUserRequester(Requester):
    def post(self, login_user_request_model: LoginUserRequest) -> LoginUserResponse:
        url = f"{self.base_url}/api/auth/token/login"
        response = requests.post(
            url=url,
            headers=self.headers,
            json=login_user_request_model.model_dump()
        )
        self.response_spec(response)
        return LoginUserResponse(**response.json())
