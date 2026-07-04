import allure
import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.fixture
def credit_user_account(api_manager: ApiManager, create_second_user_request: CreateUserRequest):
    with allure.step(f"Кредитный счет для пользователя {create_second_user_request.username} создан"):
        credit_account = api_manager.user_steps.create_account(create_second_user_request)
    return credit_account


@pytest.fixture
def credit_user_second_account(api_manager: ApiManager, create_second_user_request: CreateUserRequest):
    with allure.step(f'Второй счет для пользователя {create_second_user_request.username} создан'):
        credit_second_account = api_manager.user_steps.create_account(create_second_user_request)
    return credit_second_account
