import allure
import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account



@pytest.mark.api
class TestDeposit:
    def test_deposit_account(self, db_session: Session, api_manager: ApiManager, create_user_request, created_account: CreateAccountResponse):
        deposit_request = DepositRequest(accountId=created_account.id, amount=5000)

        with allure.step(f"Пополнение {deposit_request.amount} на счет {deposit_request.accountId}"):
            api_manager.user_steps.deposit_account(deposit_request, create_user_request)

        with allure.step("Проверка баланса на пополнение"):
            ending_account = Account.get_account_by_id(db_session, created_account.id)
            assert ending_account.balance == pytest.approx(created_account.balance + deposit_request.amount), "Пополнение не прошло"


    def test_deposit_non_existing_account(self, db_session: Session, api_manager: ApiManager, create_user_request, created_account: CreateAccountResponse):
        deposit_request = DepositRequest(accountId=created_account.id + 99999, amount=5000)

        with allure.step(f"Попытка пополнить несуществующий счет {deposit_request.accountId} "):
            response = api_manager.user_steps.deposit_nonexistent_account(deposit_request, create_user_request)

        with allure.step(f"Проверка ошибки {deposit_request.accountId}"):
            assert str(deposit_request.accountId) in response.json()["error"], f"счет {deposit_request.accountId} не найден"

        with allure.step(f"Проверка, что баланс счета {created_account.id} в БД не изменился"):
            db_session.expire_all()
            account_after = Account.get_account_by_id(db_session, created_account.id)
            assert account_after.balance == pytest.approx(created_account.balance), "Баланс счета изменился после ошибочного пополнения"

