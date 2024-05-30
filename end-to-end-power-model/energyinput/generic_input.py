from abc import ABC, abstractmethod

class GenericInput(ABC):
    @abstractmethod
    def read_energy(self) -> int:
        pass
