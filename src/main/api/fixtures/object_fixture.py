import pytest
import logging

from classes.api_manager import ApiManager
from models.create_user_response_model import CreateUserResponse
from typing import List, Any



@pytest.fixture
def created_object():
    objects: List[Any] = []
    yield objects
    clean_user(objects)

def clean_user(objects: List[Any]):
    api_manager = ApiManager(objects)
    for u in objects:
        if isinstance(u, CreateUserResponse):
            api_manager.admin_steps.delete_user(u.id)
        else:
            logging.warning(f"Error in delete user_id: {u.id}")