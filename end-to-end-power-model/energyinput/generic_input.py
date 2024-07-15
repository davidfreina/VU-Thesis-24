from abc import ABC, abstractmethod
import logging


class GenericInput(ABC):
    def __init__(self, total_energy=0):
        self.total_energy = total_energy
        self.previous_energy = 0
        self.logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        self.utilization_unit = "%"
        self.power_unit = "W"

    @abstractmethod
    def get_energy(self) -> float:
        pass

    @abstractmethod
    def get_utilization(self) -> float:
        pass
