from src.main.api.requests.credit_repay_requester import CreditRepayRequester
from models.credit_repay_request_model import CreditRepayRequest
from src.main.api.requests.credit_history_requester import CreditHistoryRequester
from src.main.api.requests.deposit_requester import DepositRequester
from src.main.api.models.deposit_request_model import DepositRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.models.create_user_request_model import CreateUserRequest
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.transactions_requester import TransactionsRequester
from src.main.api.requests.credit_requester import CreditRequester
from src.main.api.models.credit_request_model import CreditRequest

class TestCreditRepay:
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

        deposit_request = DepositRequest(
            accountId=account_id,
            amount=5000
        )

        DepositRequester(
            request_spec=RequestSpecs.auth_headers(username=user_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(deposit_request)

        transactions_response = TransactionsRequester(
            request_spec=RequestSpecs.auth_headers(username=user_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).get(account_id=account_id)

        assert transactions_response.balance == 5000 #проверяем что баланс пополнился

        credit_request = CreditRequest(
            accountId=account_id,
            amount=5000,
            termMonths=12
        )

        credit_request_response = CreditRequester(
            request_spec=RequestSpecs.auth_headers(username=user_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post(credit_request)

        credit_id = credit_request_response.creditId

        transactions_response = TransactionsRequester(
            request_spec=RequestSpecs.auth_headers(username=user_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).get(account_id=account_id)

        assert transactions_response.balance == 10000 #проверяем что баланс пополнился после кредита

        credit_history_response = CreditHistoryRequester(
            request_spec=RequestSpecs.auth_headers(username=user_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).get()

        assert credit_history_response.credits[0].balance == -5000 #проверяем что кредитный баланс пополнился

        credit_repay_request = CreditRepayRequest(
            creditId= credit_id,
            accountId= account_id,
            amount= 5000
        )

        CreditRepayRequester(
            request_spec=RequestSpecs.auth_headers(username=user_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(credit_repay_request)

        credit_history_response = CreditHistoryRequester(
            request_spec=RequestSpecs.auth_headers(username=user_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).get()

        assert credit_history_response.credits[0].balance == 0 #проверяем что кредит погашен

        transactions_response = TransactionsRequester(
            request_spec=RequestSpecs.auth_headers(username=user_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).get(account_id=account_id)

        assert transactions_response.balance == 5000 #проверяем что баланс 5000 как до взятия кредита

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

        credit_request_response = CreditRequester(
            request_spec=RequestSpecs.auth_headers(username=user_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post(credit_request)

        credit_id = credit_request_response.creditId

        credit_repay_request = CreditRepayRequest(
            creditId=credit_id,
            accountId=account_id,
            amount=500
        )

        CreditRepayRequester(
            request_spec=RequestSpecs.auth_headers(username=user_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_unprocessable_content() #проверяем что нельзя погасить кредит частями
        ).post(credit_repay_request)

        transactions_response = TransactionsRequester(
            request_spec=RequestSpecs.auth_headers(username=user_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).get(account_id=account_id)

        assert transactions_response.balance == 5000 #проверяем что кредит не погашен