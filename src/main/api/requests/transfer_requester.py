from http import HTTPStatus

import requests
from src.main.api.models.transfer_response_model import TransferResponse
from src.main.api.models.transfer_request_model import TransferRequest
from src.main.api.requests.requester import Requester


class TransferRequester(Requester):
    def post(self, transfer_request_model: TransferRequest):
        url = f"{self.base_url}/api/account/transfer"
        response = requests.post(
            url=url,
            headers=self.headers,
            json=transfer_request_model.model_dump()
        )
        self.response_spec(response)
        if response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
             return TransferResponse(**response.json())
        return response