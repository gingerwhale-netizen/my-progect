import requests
from src.main.api.configs.config import Config
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.requests.requester import Requester


class CreateAccountRequester(Requester):
    def post(self, model=None) -> CreateAccountResponse:
        response = requests.post(
            url=f"{Config.fetch('backendUrl')}/account/create",
            headers=self.request_spec,
        )
        self.response_spec(response)
        return CreateAccountResponse(**response.json())
