from typing import List

import psutil
from typing import List

from .generic_input import GenericInput


class RAPLSysFSInput(GenericInput):

    def __init__(self, rapl_files: List[str]):
        super().__init__()
        self.rapl_files = rapl_files
        self.previous_energy = self.read_energy()
        self.utilization = 0
        self.max_counter_value = 262143328850 * len(rapl_files)

    def __str__(self):
        return self.rapl_files[0].split('/').pop(-2)

    def read_energy(self) -> List[int]:
        energies = []
        for rapl_file in self.rapl_files:
            with open(rapl_file, 'r') as file:
                energies.append(int(file.read().strip()))
        return energies

    def get_energy(self) -> float:
        per_core_usage = psutil.cpu_percent(percpu=True, interval=None)
        proc_usage = 0
        for proc in psutil.process_iter(["name", "username"]):
            try:
                if "subscriber.py" in proc.cmdline():
                    proc_usage += proc.cpu_percent(interval=None)
                    self.utilization = proc_usage
            except psutil.ZombieProcess:
                continue
            except psutil.NoSuchProcess:
                continue
        energies = self.read_energy()
        current_energy = 0
        for idx, energy in enumerate(energies):
            current_energy += self.handle_overflow(energy, idx)
        self.previous_energy = energies
        return current_energy / 1000000 * (proc_usage / sum(per_core_usage))

    def handle_overflow(self, current_energy: int, index: int) -> int:
        if current_energy < self.previous_energy[index]:
            overflow_correction = self.max_counter_value - self.previous_energy[index] + current_energy + 1
            return overflow_correction
        else:
            return current_energy - self.previous_energy[index]

    def get_utilization(self) -> float:
        return self.utilization
