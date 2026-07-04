import allure
import pytest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.classes.api_manager import ApiManager

@pytest.fixture
def created_account(api_manager: ApiManager, create_user_request: CreateUserRequest):
    with allure.step(f"Счет для пользователя {create_user_request.username} создан"):
        account = api_manager.user_steps.create_account(create_user_request)
    return account

@pytest.fixture
def created_second_account(api_manager: ApiManager, create_user_request: CreateUserRequest):
    with allure.step(f"Второй счет для пользователя {create_user_request.username} создан"):
        account = api_manager.user_steps.create_account(create_user_request)
    return account
