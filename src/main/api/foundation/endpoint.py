from models.create_user_request_model import CreateUserRequest
from models.create_user_response_model import CreateUserResponse
from src.main.api.models.base_model import BaseModel
from typing import Optional, Type
from dataclasses import dataclass

@dataclass
class EndpointConfiguration:
    url: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Type[BaseModel]]

class Endpoint:
    ADMIN_CREATE_USER = EndpointConfiguration(
        request_model=CreateUserRequest,
        response_model=CreateUserResponse,
        url="/admin/create"
    )
