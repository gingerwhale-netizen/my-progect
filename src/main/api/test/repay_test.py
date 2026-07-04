import allure
import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.repay_request import RepayRequest
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.db.crud.account_crud import AccountCrudDb as Account


@pytest.mark.api
class TestRepay:
    def test_repay_credit(
            self, db_session: Session, api_manager: ApiManager,
            create_second_user_request: CreateUserRequest, credit_user_account: CreateAccountResponse):
        credit = CreditRequest(
            accountId=credit_user_account.id,
            amount=10000,
            termMonths=12
        )
        with allure.step(f'Кредит для пользователя {credit_user_account.id} создан'):
            request_credit = api_manager.user_steps.credit_request(credit, create_second_user_request)

        balance_before_repay = request_credit.balance

        repay_request = RepayRequest(
            creditId=request_credit.creditId,
            accountId=credit_user_account.id,
            amount=credit.amount
        )
        with allure.step(f'Кредит {request_credit.creditId} для пользователя {credit_user_account.id} на сумму {credit.amount} оплачен'):
            repaid = api_manager.user_steps.repay_credit(repay_request, create_second_user_request)

            db_session.expire_all()
            ending_account = Account.get_account_by_id(db_session, credit_user_account.id)

            assert repaid.amountDeposited == credit.amount, 'Сервер вернул сумму погашения, отличную от суммы кредита'
            assert ending_account.balance == pytest.approx(balance_before_repay - credit.amount), 'Погашение кредита не отразилось в БД'


    def test_repay_credit_access_denied(
            self, db_session: Session, api_manager: ApiManager,
            create_second_user_request: CreateUserRequest, credit_user_account: CreateAccountResponse
    ):
        credit = CreditRequest(
            accountId=credit_user_account.id,
            amount=10000,
            termMonths=12
        )
        with allure.step(f'Кредит для пользователя {credit_user_account.id} на сумму {credit.amount} создан'):
            request_credit = api_manager.user_steps.credit_request(credit, create_second_user_request)

        another_user = CreateUserRequest(username="Max1111new", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")
        api_manager.admin_steps.create_user(another_user)

        repay_request = RepayRequest(
            creditId=request_credit.creditId,
            accountId=credit_user_account.id,
            amount=credit.amount
        )

        with allure.step(f'Пользователь {another_user.username} пытается оплатить чужой кредит {request_credit.creditId}'):
            response = api_manager.user_steps.repay_credit_access_denied(repay_request, another_user)
        assert "not found or does not belong" in response.json()["error"], 'Сервер не подтвердил права на доступ к чужому кредиту'

        with allure.step(f'Проверка, что баланс счета {credit_user_account.id} в БД не изменился'):
            db_session.expire_all()
            ending_account = Account.get_account_by_id(db_session, credit_user_account.id)
            assert ending_account.balance == pytest.approx(request_credit.balance), 'Баланс счета изменился после отказа в доступе к чужому кредиту'