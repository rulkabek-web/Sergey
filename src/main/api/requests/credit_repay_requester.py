from http import HTTPStatus

import requests
from src.main.api.models.credit_repay_request_model import CreditRepayRequest
from src.main.api.models.credit_repay_response_model import CreditRepayResponse
from src.main.api.requests.requester import Requester


class CreditRepayRequester(Requester):
    def post(self, credit_repay_request_model: CreditRepayRequest):
        url = f"{self.base_url}/api/credit/repay"
        response = requests.post(
            url=url,
            headers=self.headers,
            json=credit_repay_request_model.model_dump()
        )
        self.response_spec(response)
        if response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
             return CreditRepayResponse(**response.json())
        return response