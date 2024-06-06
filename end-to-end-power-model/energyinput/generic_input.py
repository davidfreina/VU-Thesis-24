from abc import ABC, abstractmethod


class GenericInput(ABC):
    def __init__(self, total_energy=0):
        self.total_energy = total_energy
        self.previous_energy = 0

    @abstractmethod
    def get_energy(self) -> int:
        pass

