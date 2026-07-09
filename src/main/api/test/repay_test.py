import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.repay_request import RepayRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account


@pytest.mark.api
class TestRepay:
    def test_repay_credit(self, db_session: Session, api_manager: ApiManager, create_second_user_request, created_credit, repay_request: RepayRequest):
        repaid = api_manager.user_steps.repay_credit(repay_request, create_second_user_request)

        db_session.expire_all()
        account_from_db = Account.get_account_by_id(db_session, repay_request.accountId)
        assert repaid.amountDeposited == repay_request.amount, "Сервер вернул сумму погашения, отличную от запрошенной"
        assert account_from_db.balance == 0, "После полного погашения баланс счёта должен вернуться к 0"

    def test_repay_credit_access_denied(self, api_manager: ApiManager, another_credit_user, repay_request: RepayRequest):
        response = api_manager.user_steps.repay_credit_access_denied(repay_request, another_credit_user)
        assert "not found or does not belong" in response.json()["error"], "Сервер не защитил чужой кредит от постороннего пользователя"
