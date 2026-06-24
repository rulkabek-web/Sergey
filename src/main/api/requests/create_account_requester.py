import requests
from src.main.api.requests.requester import Requester
from models.create_account_response_model import CreateAccountResponse


class CreateAccountRequester(Requester):
    def post(self, model=None)->CreateAccountResponse:
        url=f"{self.base_url}/api/account/create"
        response = requests.post(
            url=url,
            headers=self.headers,
        )
        self.response_spec(response)
        return CreateAccountResponse(**response.json())