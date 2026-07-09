import allure
import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.repay_request import RepayRequest
from src.main.api.generators.model_generator import RandomModelGenerator


@pytest.fixture
def credit_user_account(api_manager: ApiManager, create_second_user_request: CreateUserRequest):
    with allure.step(f"Кредитный счет для пользователя {create_second_user_request.username} создан"):
        return api_manager.user_steps.create_account(create_second_user_request)


@pytest.fixture
def credit_user_second_account(api_manager: ApiManager, create_second_user_request: CreateUserRequest):
    with allure.step(f"Второй счет для пользователя {create_second_user_request.username} создан"):
        return api_manager.user_steps.create_account(create_second_user_request)


@pytest.fixture
def credit_request(credit_user_account):
    return CreditRequest(
        accountId=credit_user_account.id,
        amount=RandomModelGenerator.generate_credit_amount(),
        termMonths=RandomModelGenerator.generate_term_months(),
    )


@pytest.fixture
def second_credit_request(credit_user_second_account):
    return CreditRequest(
        accountId=credit_user_second_account.id,
        amount=RandomModelGenerator.generate_credit_amount(),
        termMonths=RandomModelGenerator.generate_term_months(),
    )


@pytest.fixture
def created_credit(api_manager, credit_request, create_second_user_request):
    with allure.step("Предусловие: кредит оформлен"):
        return api_manager.user_steps.credit_request(credit_request, create_second_user_request)


@pytest.fixture
def repay_request(created_credit):
    return RepayRequest(
        creditId=created_credit.creditId,
        accountId=created_credit.id,
        amount=created_credit.amount,
    )
