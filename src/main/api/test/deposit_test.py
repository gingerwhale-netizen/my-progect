import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account


@pytest.mark.api
class TestDeposit:
    def test_deposit_account(self, db_session: Session, api_manager: ApiManager, create_user_request, deposit_request: DepositRequest):
        deposit_response = api_manager.user_steps.deposit_account(deposit_request, create_user_request)

        account_from_db = Account.get_account_by_id(db_session, deposit_request.accountId)
        assert account_from_db.balance == deposit_response.balance, "Баланс в БД не совпал с ответом сервера"

    def test_deposit_non_existing_account(self, api_manager: ApiManager, create_user_request, deposit_request: DepositRequest):
        deposit_request.accountId += 99999  # несуществующий счёт

        response = api_manager.user_steps.deposit_nonexistent_account(deposit_request, create_user_request)
        assert str(deposit_request.accountId) in response.json()["error"], "Сервер не сообщил, что счёт не найден"
