from .generic_input import GenericInput


class RAPLSysFSInput(GenericInput):
    max_counter_value = 2 ** 64 - 1  # Assuming a 64-bit counter for RAPL

    def __init__(self, rapl_file: str):
        super().__init__()
        self.rapl_file = rapl_file
        self.previous_energy = self.read_energy()

    def __str__(self):
        return self.rapl_file.split('/').pop(-2)

    def read_energy(self) -> int:
        with open(self.rapl_file, 'r') as file:
            energy = int(file.read().strip())
        return energy

    def handle_overflow(self, current_energy: int) -> int:
        if current_energy < self.previous_energy:
            overflow_correction = self.max_counter_value - self.previous_energy + current_energy + 1
            return overflow_correction
        else:
            return current_energy - self.previous_energy
