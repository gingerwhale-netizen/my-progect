from typing import Any


class BaseSteps:
    def __init__(self, created_obj: list[Any]):
        self.created_obj = created_obj
