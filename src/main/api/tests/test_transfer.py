import pytest

from src.main.api.requests.transactions_requester import TransactionsRequester
from src.main.api.requests.transfer_requester import TransferRequester
from src.main.api.requests.deposit_requester import DepositRequester
from src.main.api.models.deposit_request_model import DepositRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.models.create_user_request_model import CreateUserRequest
from src.main.api.models.login_user_request_model import LoginUserRequest
from src.main.api.requests.login_user_requester import LoginUserRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.models.transfer_request_model import TransferRequest

class TestTransfer:
    def test_transfer_valid(self):

        user_username = "Gieo2"
        another_user_username = "Aynd2"

        create_user_request = CreateUserRequest(
            username=user_username,
            password="Pas!sw0rd",
            role="ROLE_USER"
        )

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        create_account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=user_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        assert create_account_response.balance == 0
        account_id = create_account_response.id

        deposit_request = DepositRequest(
            accountId=account_id,
            amount=1000.5
        )

        deposit_response = DepositRequester(
            request_spec=RequestSpecs.auth_headers(username=user_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(deposit_request)


        assert deposit_response.balance == deposit_request.amount #проверяем что баланс пополнился на 1000,5

        create_another_user_request = CreateUserRequest(
            username=another_user_username,
            password="Pas!sw0rd",
            role="ROLE_USER"
        )

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_another_user_request)

        login_another_user_request = LoginUserRequest(
            username=another_user_username,
            password="Pas!sw0rd",
        )

        LoginUserRequester(
            request_spec=RequestSpecs.unauth_headers(),
            response_spec=ResponseSpecs.request_ok()
        ).post(login_another_user_request)

        create_another_account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=another_user_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        another_account_id = create_another_account_response.id

        transfer_request = TransferRequest(
            fromAccountId= account_id,
            toAccountId= another_account_id,
            amount= 500.75
        )

        transfer_response = TransferRequester(
            request_spec=RequestSpecs.auth_headers(username=user_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(transfer_request)

        assert transfer_response.fromAccountIdBalance == deposit_response.balance-transfer_request.amount #проверяем баланс после перевода

        transactions_response = TransactionsRequester(
            request_spec=RequestSpecs.auth_headers(username=another_user_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).get(account_id=another_account_id)

        assert transactions_response.balance == transfer_request.amount #проверяем что перевод дошел другому пользователю

    @pytest.mark.parametrize(
        "transfer_amount, user_username, another_user_username",
        [
            (499, "Geor2", "Ande2"),
            (11000, "Geor3", "Ande3"),
        ]
    )
    def test_transfer_invalid(self, transfer_amount, user_username, another_user_username):

        create_user_request = CreateUserRequest(
            username=user_username,
            password="Pas!sw0rd",
            role="ROLE_USER"
        )

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        create_account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=user_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        account_id = create_account_response.id

        deposit_request = DepositRequest(
            accountId=account_id,
            amount=8000
        )

        deposit_response = DepositRequester(
            request_spec=RequestSpecs.auth_headers(username=user_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(deposit_request)

        assert deposit_response.balance == 8000 #проверяем баланс после пополнения

        deposit_response = DepositRequester(
            request_spec=RequestSpecs.auth_headers(username=user_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(deposit_request)

        assert deposit_response.balance == 16000 #проверяем баланс после 2 пополнения

        create_another_user_request = CreateUserRequest(
            username=another_user_username,
            password="Pas!sw0rd",
            role="ROLE_USER"
        )

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_another_user_request)

        create_another_account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=another_user_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        another_account_id = create_another_account_response.id

        transfer_request = TransferRequest(
            fromAccountId=account_id,
            toAccountId=another_account_id,
            amount=transfer_amount
        )

        TransferRequester(
            request_spec=RequestSpecs.auth_headers(username=user_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_bad() #проверяем что не можем перевести меньше 500 или больше 10000. Получаем 400 код 
        ).post(transfer_request)



