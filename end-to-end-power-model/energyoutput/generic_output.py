from abc import ABC, abstractmethod

class GenericOutput(ABC):
    @abstractmethod
    def report_energy(self, device: str, energy: int) -> None:
        pass