import allure
import pytest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.transfer_request import TransferRequest
from sqlalchemy.orm import Session
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestTransfer:
    def test_transfer(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, created_account: CreateAccountResponse, created_second_account: CreateAccountResponse):
        with allure.step(f'Пополнение счета отправителя {created_account.id} перед переводом'):
            deposit_request = DepositRequest(accountId=created_account.id, amount=5000)
            api_manager.user_steps.deposit_account(deposit_request, create_user_request)

            account_before_transfer = Account.get_account_by_id(db_session, created_account.id)
            balance_before_transfer = account_before_transfer.balance

        transfer = TransferRequest(
            fromAccountId=created_account.id,
            toAccountId=created_second_account.id,
            amount=1000
        )

        with allure.step(f'Перевод на сумму {transfer.amount} между счетами {transfer.fromAccountId} и {transfer.toAccountId} совершен'):
            api_manager.user_steps.transfer(transfer_request=transfer, create_user_request=create_user_request)

            db_session.expire_all()     #сбрасываем кэш и  заставляем зайти в БД заново
            ending_from_account = Account.get_account_by_id(db_session, created_account.id)
            ending_to_account = Account.get_account_by_id(db_session, created_second_account.id)

        assert ending_to_account.balance == pytest.approx(created_second_account.balance + transfer.amount), 'Ошибка пополнения'
        assert ending_from_account.balance == pytest.approx(balance_before_transfer - transfer.amount), 'Ошибка отправки перевода'


    def test_insufficient_funds_transfer(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, created_account: CreateAccountResponse, created_second_account: CreateAccountResponse):
        transfer_request = TransferRequest(fromAccountId=created_account.id, toAccountId=created_second_account.id, amount=5000)
        with allure.step(f'Попытка перевести {transfer_request.amount} со счета {created_account.id} с балансом {created_account.balance}'):
            response = api_manager.user_steps.insufficient_funds_transfer(transfer_request, create_user_request)

            assert "Insufficient funds" in response.json()["error"], f"Сумма перевода {transfer_request.amount} больше баланса счета {created_account.balance}"

        with allure.step('Проверка, что балансы счетов в БД не изменились'):
            db_session.expire_all()
            ending_from_account = Account.get_account_by_id(db_session, created_account.id)
            ending_to_account = Account.get_account_by_id(db_session, created_second_account.id)
            assert ending_from_account.balance == pytest.approx(created_account.balance), 'Баланс счета отправителя изменился после ошибочного перевода'
            assert ending_to_account.balance == pytest.approx(created_second_account.balance), 'Баланс счета получателя изменился после ошибочного перевода'


