import allure

from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.repay_request import RepayRequest
from src.main.api.models.repay_response import RepayResponse
from src.main.api.specs.requests_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        with allure.step(f'Счет для пользователя {create_user_request.username} создан'):
            response = ValidateCrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.CREATE_ACCOUNT,
                ResponseSpecs.request_created()
            ).post(None)
            return response

    def deposit_account(self, deposit_request: DepositRequest, create_user_request: CreateUserRequest):
        with allure.step(f'Пополнение счета {create_user_request.username} на сумму {deposit_request.amount}'):
            response = ValidateCrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.DEPOSIT_ACCOUNT,
                ResponseSpecs.request_ok()
            ).post(deposit_request)
            return response

    def deposit_nonexistent_account(self, deposit_request: DepositRequest, create_user_request: CreateUserRequest):
        with allure.step(f'Ошибка пополнения, указанный номер счета {deposit_request.accountId} не найден'):
            response = CrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.DEPOSIT_ACCOUNT,
                ResponseSpecs.request_not_found()
            ).post(deposit_request)
            return response

    def transfer(self, transfer_request: TransferRequest, create_user_request: CreateUserRequest):
        with allure.step(f'Осуществлен перевод на сумму {transfer_request.amount} со счета {transfer_request.fromAccountId} на счет {transfer_request.toAccountId}'):
            response = ValidateCrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.TRANSFER_ACCOUNT,
                ResponseSpecs.request_ok()
            ).post(transfer_request)
            return response

    def insufficient_funds_transfer(self, transfer_request: TransferRequest, create_user_request: CreateUserRequest):
        with allure.step(f'Ошибка транзакции, сумма перевода {transfer_request.amount}, больше баланса счета {transfer_request.fromAccountId}'):
            response = CrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.TRANSFER_ACCOUNT,
                ResponseSpecs.request_insufficient_funds()
            ).post(transfer_request)
            return response

    def credit_request(self, credit_request: CreditRequest, create_second_user_request: CreateUserRequest):
        with allure.step(f'Запрос на кредит от пользователя {create_second_user_request.username}'):
            response = ValidateCrudRequester(
                RequestSpecs.auth_headers(username=create_second_user_request.username, password=create_second_user_request.password),
                Endpoint.CREDIT_REQUEST,
                ResponseSpecs.request_created()
            ).post(credit_request)
            return response

    def credit_request_already_exists(self, credit_request: CreditRequest, create_second_user_request: CreateUserRequest):
        with allure.step(f'Запрос для пользователя {create_second_user_request.username} на второй кредит отклонен'):
            response = CrudRequester(
                RequestSpecs.auth_headers(username=create_second_user_request.username, password=create_second_user_request.password),
                Endpoint.CREDIT_REQUEST,
                ResponseSpecs.request_forbidden_as_not_found()
            ).post(credit_request)
            return response

    def repay_credit(self, repay_request: RepayRequest, create_second_user_request: CreateUserRequest):
        with allure.step(f'Погашение кредита {repay_request.creditId} пользователя {create_second_user_request.username}'):
            response = ValidateCrudRequester(
                RequestSpecs.auth_headers(username=create_second_user_request.username, password=create_second_user_request.password),
                Endpoint.CREDIT_REPAY,
                ResponseSpecs.request_ok()
            ).post(repay_request)
            return response

    def repay_credit_access_denied(self, repay_request: RepayRequest, create_user_request: CreateUserRequest):
        with allure.step(f'Попытка погасить пользователем {create_user_request.username} чужой кредит {repay_request.creditId}'):
            response = CrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.CREDIT_REPAY,
                ResponseSpecs.request_forbidden_as_not_found()
            ).post(repay_request)
            return response
