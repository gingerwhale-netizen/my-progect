import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.credit_request import CreditRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account


@pytest.mark.api
class TestCredit:
    def test_credit_account(self, db_session: Session, api_manager: ApiManager, create_second_user_request, credit_request: CreditRequest):
        credit_response = api_manager.user_steps.credit_request(credit_request, create_second_user_request)

        account_from_db = Account.get_account_by_id(db_session, credit_request.accountId)
        assert account_from_db.balance == credit_response.balance, "Баланс в БД не совпал с ответом сервера"

    def test_credit_request_already_exists(self, api_manager: ApiManager, create_second_user_request, created_credit, second_credit_request: CreditRequest):
        response = api_manager.user_steps.credit_request_already_exists(second_credit_request, create_second_user_request)
        assert "Only one active credit allowed per user" in response.json()["error"], "Сервер разрешил второй активный кредит"
