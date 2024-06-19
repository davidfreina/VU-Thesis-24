from abc import ABC, abstractmethod

class GenericOutput(ABC):
    @abstractmethod
    def report_power(self, device: str, power: int) -> None:
        pass