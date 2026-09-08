class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def getInstance(cls):
        return cls()

    def log(self, message):
        print(f"[MES] {message}")