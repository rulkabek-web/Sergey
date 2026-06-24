from src.main.api.requests.transactions_requester import TransactionsRequester
from src.main.api.models.credit_request_model import CreditRequest
from src.main.api.requests.transfer_requester import TransferRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.models.create_user_request_model import CreateUserRequest
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.models.transfer_request_model import TransferRequest
from src.main.api.requests.credit_requester import CreditRequester

class TestCreditRequest:
    def test_valid_credit_request(self):
        user_username = "Sergey23"

        create_user_request = CreateUserRequest(
            username=user_username,
            password="Pas!sw0rd",
            role="ROLE_CREDIT_SECRET"
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

        credit_request = CreditRequest(
            accountId=account_id,
            amount=5000,
            termMonths=12
        )

        CreditRequester(
            request_spec=RequestSpecs.auth_headers(username=user_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post(credit_request)

        transactions_response = TransactionsRequester(
            request_spec=RequestSpecs.auth_headers(username=user_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).get(account_id=account_id)

        assert transactions_response.balance == credit_request.amount #проверяем что баланс пополнился на сумму кредита

        create_another_account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=user_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        another_account_id = create_another_account_response.id

        transfer_request = TransferRequest(
            fromAccountId=account_id,
            toAccountId=another_account_id,
            amount=1000
        )

        transfer_response = TransferRequester(
            request_spec=RequestSpecs.auth_headers(username=user_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(transfer_request)

        assert transfer_response.fromAccountIdBalance == 4000 #проверяем что баланс уменьшился на сумму перевода

    def test_invalid_credit_request(self):
        user_username = "Sergey23"

        create_user_request = CreateUserRequest(
            username=user_username,
            password="Pas!sw0rd",
            role="ROLE_CREDIT_SECRET"
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

        credit_request = CreditRequest(
            accountId=account_id,
            amount=5000,
            termMonths=12
        )

        CreditRequester(
            request_spec=RequestSpecs.auth_headers(username=user_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post(credit_request)

        another_credit_request = CreditRequest(
            accountId=account_id,
            amount=5000,
            termMonths=12
        )

        CreditRequester(
            request_spec=RequestSpecs.auth_headers(username=user_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_not_found() #проверяем что не можем взять 2 кредит на аккаунт, получаем код 404 вместо 403:Уже есть активный кредит
        ).post(another_credit_request)





