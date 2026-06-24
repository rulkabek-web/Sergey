import requests

from src.main.api.configs.config import Config
from src.main.api.models.login_user_request_model import LoginUserRequest
from src.main.api.models.login_user_response_model import LoginUserResponse

class RequestSpecs:

    @staticmethod
    def base_headers():
        return {
                "accept": "application/json",
                "Content-Type": "application/json"
            }

    @staticmethod
    def auth_headers(username: str, password: str):
        login_request = LoginUserRequest(username=username, password=password)
        login_admin_response = requests.post(
            url=f"{Config.fetch("backendUrl")}/api/auth/token/login",
            json=login_request.model_dump(),
            headers=RequestSpecs.base_headers()
        )
        if login_admin_response.status_code == 200:
            response_data = LoginUserResponse(**login_admin_response.json())
            token = response_data.token
            headers = RequestSpecs.base_headers()
            headers["Authorization"] = f"Bearer {token}"

            return {
                "headers": headers,
                "base_url": Config.fetch("backendUrl")
            }
        raise Exception("!!! Authentication failed !!!")

    @staticmethod
    def unauth_headers():
        return {
            "headers": RequestSpecs.base_headers(),
            "base_url": Config.fetch("backendUrl")
        }