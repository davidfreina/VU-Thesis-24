from .generic_input import GenericInput

class RAPLSysFSInput(GenericInput):
    def __init__(self, rapl_file: str):
        self.rapl_file = rapl_file
        self.previous_energy = self.read_energy()

    def read_energy(self) -> int:
        with open(self.rapl_file, 'r') as file:
            energy = int(file.read().strip())
        return energy

