from http import HTTPStatus

import requests
from src.main.api.models.deposit_response_model import DepositResponse
from src.main.api.models.deposit_request_model import DepositRequest
from src.main.api.requests.requester import Requester


class DepositRequester(Requester):
    def post(self, deposit_request_model: DepositRequest):
        url = f"{self.base_url}/api/account/deposit"
        response = requests.post(
            url=url,
            headers=self.headers,
            json=deposit_request_model.model_dump()
        )
        self.response_spec(response)
        if response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
             return DepositResponse(**response.json())
        return response