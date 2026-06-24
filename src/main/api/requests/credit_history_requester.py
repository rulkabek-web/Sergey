from http import HTTPStatus

import requests
from src.main.api.models.credit_history_response_model import CreditHistoryResponse
from src.main.api.requests.requester import Requester


class CreditHistoryRequester(Requester):
    def get(self):
        url = f"{self.base_url}/api/credit/history"
        response = requests.get(
            url=url,
            headers=self.headers
        )
        self.response_spec(response)
        if response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
             return CreditHistoryResponse(**response.json())
        return response

    def post(self, model=None):
        raise NotImplementedError("POST is not supported for TransactionsRequester")