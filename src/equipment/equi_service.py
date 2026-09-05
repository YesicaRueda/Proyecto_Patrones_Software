

from infrastructure.logger import Logger


class EquipmentService:

    def start_machine(self, machine_id):
        logger = Logger.getInstance()
        logger.log(f"Máquina {machine_id} en operación")