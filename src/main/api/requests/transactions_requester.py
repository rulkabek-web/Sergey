from http import HTTPStatus

import requests
from src.main.api.models.transactions_response_model import TransactionsResponse
from src.main.api.requests.requester import Requester


class TransactionsRequester(Requester):
    def get(self, account_id):
        url = f"{self.base_url}/api/account/transactions/{account_id}"
        response = requests.get(
            url=url,
            headers=self.headers
        )
        self.response_spec(response)
        if response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
             return TransactionsResponse(**response.json())
        return response

    def post(self, model=None):
        raise NotImplementedError("POST is not supported for TransactionsRequester")