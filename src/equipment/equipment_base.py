from abc import ABC, abstractmethod


class Equipment(ABC):

    def __init__(self):
        self.status = "Parada"

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass


class Inspection(ABC):

    @abstractmethod
    def inspect(self, order) -> bool:
        pass
