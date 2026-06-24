from src.main.api.requests.deposit_requester import DepositRequester
from src.main.api.models.deposit_request_model import DepositRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.models.create_user_request_model import CreateUserRequest
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.create_account_requester import CreateAccountRequester

class TestDeposit:
    def test_deposit_valid(self):
        user_username = "Gieo2"

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

        user_account_id = create_account_response.id

        deposit_request = DepositRequest(
            accountId=user_account_id,
            amount=1000.5
        )

        deposit_response = DepositRequester(
            request_spec=RequestSpecs.auth_headers(username=user_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(deposit_request)

        assert deposit_response.balance == deposit_request.amount #проверяем что успешно пополнили счет

    def test_deposit_invalid(self):

        user_username = "Ser92"
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

        user_account_id = create_account_response.id

        deposit_request = DepositRequest(
            accountId=user_account_id,
            amount=1000.5
        )

        DepositRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_forbidden() #не можем депозитнуть админом получаем 403 код
        ).post(deposit_request)

        create_another_user_request = CreateUserRequest(
            username=another_user_username,
            password="Pas!sw0rd",
            role="ROLE_USER"
        )

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_another_user_request)

        another_create_account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=another_user_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        another_user_account_id = another_create_account_response.id

        deposit_request = DepositRequest(
            accountId=another_user_account_id,
            amount=1000.5
        )

        DepositRequester(
            request_spec=RequestSpecs.auth_headers(username=user_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_not_found()  # не можем депозитнуть другим юзером получаем 404 код
        ).post(deposit_request)







