from http import HTTPStatus
from requests import Response
import requests
from src.main.api.models.credit_response_model import CreditResponse
from src.main.api.models.credit_request_model import CreditRequest
from src.main.api.requests.requester import Requester


class CreditRequester(Requester):
    def post(self, credit_request_model: CreditRequest):
        url = f"{self.base_url}/api/credit/request"
        response = requests.post(
            url=url,
            headers=self.headers,
            json=credit_request_model.model_dump()
        )
        self.response_spec(response)
        if response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
             return CreditResponse(**response.json())
        return response