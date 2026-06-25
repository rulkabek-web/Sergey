import pytest

from src.main.api.models.create_user_request_model import CreateUserRequest

class TestTry:
    def test_try(self, api_manager):


        create_user_request = CreateUserRequest(
            username="Gieo2",
            password="Pas!sw0rd",
            role="ROLE_USER"
        )
        create_user_response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_response.username == create_user_request.username


