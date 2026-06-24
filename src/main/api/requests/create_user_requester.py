from http import HTTPStatus

import requests
from src.main.api.models.create_user_response_model import CreateUserResponse
from src.main.api.models.create_user_request_model import CreateUserRequest
from src.main.api.requests.requester import Requester


class CreateUserRequester(Requester):
    def post(self, create_user_request_model: CreateUserRequest):
        url = f"{self.base_url}/api/admin/create"
        response = requests.post(
            url=url,
            headers=self.headers,
            json=create_user_request_model.model_dump()
        )
        self.response_spec(response)
        if response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
             return CreateUserResponse(**response.json())
        return response