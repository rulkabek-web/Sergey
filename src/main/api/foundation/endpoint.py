from enum import Enum

from models.create_user_request_model import CreateUserRequest
from models.create_user_response_model import CreateUserResponse
from src.main.api.models.login_user_request_model import LoginUserRequest
from src.main.api.models.login_user_response_model import LoginUserResponse

from src.main.api.models.base_model import BaseModel
from typing import Optional, Type
from dataclasses import dataclass

@dataclass
class EndpointConfiguration:
    url: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Type[BaseModel]]

class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfiguration(
        request_model=CreateUserRequest,
        response_model=CreateUserResponse,
        url="/admin/create"
    )
    LOGIN_USER = EndpointConfiguration(
        request_model=LoginUserRequest,
        response_model=LoginUserResponse,
        url="/auth/token/login"
    )
    ADMIN_DELETE_USER = EndpointConfiguration(
        request_model=None,
        response_model=None,
        url="/admin/users"
    )
