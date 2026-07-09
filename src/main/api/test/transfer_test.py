import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account


@pytest.mark.api
class TestTransfer:
    def test_transfer(self, db_session: Session, api_manager: ApiManager, create_user_request, transfer_request: TransferRequest):
        transfer_response = api_manager.user_steps.transfer(transfer_request, create_user_request)

        db_session.expire_all()
        from_account_from_db = Account.get_account_by_id(db_session, transfer_request.fromAccountId)
        assert from_account_from_db.balance == transfer_response.fromAccountIdBalance, "Баланс отправителя в БД не совпал с ответом сервера"

    def test_insufficient_funds_transfer(self, api_manager: ApiManager, create_user_request, transfer_request_no_funds: TransferRequest):
        response = api_manager.user_steps.insufficient_funds_transfer(transfer_request_no_funds, create_user_request)
        assert "Insufficient funds" in response.json()["error"], "Сервер не сообщил о недостатке средств"
