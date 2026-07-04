import pytest
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.fixture
def create_user_request(api_manager):
    user_request = CreateUserRequest(username="Max7fhye34", password="Pas!sw0rd", role="ROLE_USER")
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def create_second_user_request(api_manager):
    second_user_request = CreateUserRequest(username="Max777new", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")
    api_manager.admin_steps.create_user(second_user_request)
    return second_user_request
