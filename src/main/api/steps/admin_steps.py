from foundation.endpoint import Endpoint
from foundation.requesters.validate_crud_requester import ValidateCrudRequester
from foundation.requesters.crud_requester import CrudRequester

from models.create_user_request_model import CreateUserRequest
from src.main.api.steps.base_steps import BaseSteps
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.specs.request_specs import RequestSpecs


class AdminSteps(BaseSteps):
    def create_user(self, create_user_request: CreateUserRequest):
        create_user_response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok(),
            endpoint=Endpoint.ADMIN_CREATE_USER
        ).post(create_user_request)

        self.created_object.append(create_user_response)
        return create_user_response

    def delete_user(self, user_id: int):
        CrudRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok(),
            endpoint=Endpoint.ADMIN_DELETE_USER
        ).delete(user_id)