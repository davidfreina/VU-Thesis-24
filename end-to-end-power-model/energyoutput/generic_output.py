from abc import ABC, abstractmethod

class GenericOutput(ABC):
    @abstractmethod
    def report_energy(self, device: str, current: int, energy: int) -> None:
        pass