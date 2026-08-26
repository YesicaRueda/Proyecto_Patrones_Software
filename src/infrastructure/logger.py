class Logger:
    _instance = None

    def __init__(self):
        if Logger._instance is not None:
            raise Exception("Esta clase es un Singleton. Use getInstance().")

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def log(self, message):
        print(f"[MES] {message}")