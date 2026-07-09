from abc import ABC, abstractmethod
from typing import Dict, Callable
from src.main.api.models.base_model import BaseModel


class Requester(ABC):
    def __init__(self, request_spec: Dict, response_spec: Callable):
        self.request_spec = request_spec
        self.response_spec = response_spec

    @abstractmethod
    def post(self, model: BaseModel): ...
