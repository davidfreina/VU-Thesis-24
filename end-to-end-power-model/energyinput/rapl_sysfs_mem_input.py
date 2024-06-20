import psutil

from .generic_input import GenericInput


class RAPLSysFSMemInput(GenericInput):
    max_counter_value = 65712999613

    def __init__(self, rapl_file: str):
        super().__init__()
        self.rapl_file = rapl_file
        self.previous_energy = self.read_energy()
        self.current_energy = 0
        self.utilization = 0

    def __str__(self):
        return self.rapl_file.split('/').pop(-2)

    def read_energy(self) -> int:
        with open(self.rapl_file, 'r') as file:
            energy = int(file.read().strip())
        return energy

    def get_energy(self) -> float:
        total_energy = self.read_energy()
        self.current_energy = self.handle_overflow(total_energy)
        self.previous_energy = total_energy
        return self.current_energy / 1000000

    def handle_overflow(self, current_energy: int) -> int:
        if current_energy < self.previous_energy:
            overflow_correction = self.max_counter_value - self.previous_energy + current_energy + 1
            return overflow_correction
        else:
            return current_energy - self.previous_energy

    def get_utilization(self) -> float:
        return self.utilization