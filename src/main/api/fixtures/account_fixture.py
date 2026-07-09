import allure
import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.generators.model_generator import RandomModelGenerator


@pytest.fixture
def created_account(api_manager: ApiManager, create_user_request: CreateUserRequest):
    with allure.step(f"Счет для пользователя {create_user_request.username} создан"):
        return api_manager.user_steps.create_account(create_user_request)


@pytest.fixture
def created_second_account(api_manager: ApiManager, create_user_request: CreateUserRequest):
    with allure.step(f"Второй счет для пользователя {create_user_request.username} создан"):
        return api_manager.user_steps.create_account(create_user_request)


@pytest.fixture
def deposit_request(created_account):
    return DepositRequest(
        accountId=created_account.id,
        amount=RandomModelGenerator.generate_deposit_amount(),
    )


@pytest.fixture
def transfer_request(api_manager, create_user_request, created_account, created_second_account):
    with allure.step(f"Предусловие: пополнение счета отправителя {created_account.id}"):
        api_manager.user_steps.deposit_account(
            DepositRequest(accountId=created_account.id, amount=RandomModelGenerator.generate_deposit_amount()),
            create_user_request,
        )
    return TransferRequest(
        fromAccountId=created_account.id,
        toAccountId=created_second_account.id,
        amount=RandomModelGenerator.generate_transfer_amount(),
    )


@pytest.fixture
def transfer_request_no_funds(created_account, created_second_account):
    return TransferRequest(
        fromAccountId=created_account.id,
        toAccountId=created_second_account.id,
        amount=RandomModelGenerator.generate_transfer_amount(),
    )
