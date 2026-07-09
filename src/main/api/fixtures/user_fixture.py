import pytest

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.generators.model_generator import RandomModelGenerator


def _create_user(api_manager, role):
    user = RandomModelGenerator.generate(CreateUserRequest)
    user.role = role
    api_manager.admin_steps.create_user(user)
    return user


@pytest.fixture
def create_user_request(api_manager):
    return _create_user(api_manager, "ROLE_USER")


@pytest.fixture
def create_second_user_request(api_manager):
    return _create_user(api_manager, "ROLE_CREDIT_SECRET")


@pytest.fixture
def another_credit_user(api_manager):
    return _create_user(api_manager, "ROLE_CREDIT_SECRET")
