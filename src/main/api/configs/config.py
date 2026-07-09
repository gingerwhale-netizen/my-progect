from pathlib import Path
from typing import Any, Dict

class Config:
    _isinstanse = None
    _dictionary = {}

    def __new__(cls):
        if cls._isinstanse is None:
            cls._isinstanse = super(Config, cls).__new__(cls)

            config_path = Path(__file__).parents[4] / "resourses" / "urls.properties"

            if not config_path.exists():
                raise FileNotFoundError(f"Config path not found: {config_path}")

            with open(config_path, "r") as f:
                for line in f:
                    if "=" in line:
                        key, value = line.split("=", 1)
                        cls._dictionary[key.strip()] = value.strip()

        return cls._isinstanse

    @staticmethod
    def fetch(key: str, default_value: Any = None) -> Any:
            return Config()._dictionary.get(key, default_value)

