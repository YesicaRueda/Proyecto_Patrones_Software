
from src.infrastructure.logging_adapter import StandardLoggingAdapter


class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._adapter = StandardLoggingAdapter()
        return cls._instance

    @classmethod
    def getInstance(cls):
        return cls()

    def log(self, message, level="INFO"):
        self._adapter.write(message, level)