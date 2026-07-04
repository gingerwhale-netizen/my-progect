import allure
import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.db.crud.account_crud import AccountCrudDb as Account



@pytest.mark.api
class TestCredit:
    def test_credit_account(
            self, db_session: Session, api_manager: ApiManager,
            create_second_user_request: CreateUserRequest, credit_user_account: CreateAccountResponse
    ):
        credit = CreditRequest(accountId=credit_user_account.id, amount=10000, termMonths=12)

        with allure.step(f'Кредит для пользователя {credit_user_account.id} на сумму {credit.amount}'):
            requested_credit = api_manager.user_steps.credit_request(credit, create_second_user_request)

        db_session.expire_all()     # сбрасываем кэш, чтобы прочитать актуальные данные из БД
        ending_credit_account = Account.get_account_by_id(db_session, credit_user_account.id)
        assert requested_credit.balance == credit_user_account.balance + credit.amount, "Баланс в ответе сервера не совпадает с ожидаемым"
        assert ending_credit_account.balance == credit_user_account.balance + credit.amount, "Кредит не отразился в БД"
        assert requested_credit.creditId is not None, "creditId не был присвоен — кредит не создан"


    def test_credit_request_already_exists(
            self, db_session: Session, api_manager: ApiManager, credit_user_second_account: CreateAccountResponse,
            credit_user_account: CreateAccountResponse, create_second_user_request: CreateUserRequest
    ):
        credit = CreditRequest(accountId=credit_user_account.id, amount=10000, termMonths=12)
        credit_second = CreditRequest(accountId=credit_user_second_account.id, amount=10000, termMonths=12)

        with allure.step(f'Первый (активный) кредит для пользователя {credit_user_account.id} на сумму {credit.amount}'):
            # создаём первый активный кредит, чтобы повторный запрос был отклонён
            api_manager.user_steps.credit_request(credit, create_second_user_request)

        with allure.step('Повторный запрос кредита отклонён'):
            duplicate_credit_response = api_manager.user_steps.credit_request_already_exists(credit_second, create_second_user_request)
            assert "Only one active credit allowed per user" in duplicate_credit_response.json()["error"], f'У пользователя {credit_user_account.id} уже есть кредит'

        with allure.step(f'Проверка, что баланс счета {credit_user_second_account.id} в БД не изменился'):
            db_session.expire_all()
            second_account = Account.get_account_by_id(db_session, credit_user_second_account.id)
            assert second_account.balance == pytest.approx(credit_user_second_account.balance), 'Баланс счета изменился после отклонённого кредита'
