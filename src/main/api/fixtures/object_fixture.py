import logging
import pytest
from typing import Any
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.classes.api_manager import ApiManager


@pytest.fixture
def created_obj():
    objects: list[Any] = []
    yield objects
    cleanup(objects)

def cleanup(objects: list[Any]):
    api_manager = ApiManager(objects)
    for u in objects:
        if isinstance(u, CreateUserResponse):
            api_manager.admin_steps.delete_user(u.id)
        else:
            logging.warning(f"Пропуск очистки для неопознанного объекта: {u}")

