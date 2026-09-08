from abc import ABC, abstractmethod

from src.equipment.equipment_base import Equipment, Inspection


class CNCMachine(Equipment):

    def start(self):
        self.status = "Operando"
        print("Ciclo de mecanizado iniciado")

    def stop(self):
        self.status = "Parada"
        print("Ciclo de mecanizado detenido")


class CNCInspection(Inspection):

    def inspect(self, order) -> bool:
        print("Inspección dimensional realizada")
        return True


class RobotArm(Equipment):

    def start(self):
        self.status = "Operando"
        print("Ciclo de robot iniciado")

    def stop(self):
        self.status = "Parada"
        print("Ciclo de robot detenido")


class RobotInspection(Inspection):

    def inspect(self, order) -> bool:
        print("Inspección de ensamble realizada")
        return True


class AbstractProductionCellFactory(ABC):

    @abstractmethod
    def create_equipment(self):
        pass

    @abstractmethod
    def create_inspection(self):
        pass


class CNCCellFactory(AbstractProductionCellFactory):

    def create_equipment(self):
        return CNCMachine()

    def create_inspection(self):
        return CNCInspection()


class RobotCellFactory(AbstractProductionCellFactory):

    def create_equipment(self):
        return RobotArm()

    def create_inspection(self):
        return RobotInspection()
