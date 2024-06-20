import psutil

from .generic_input import GenericInput


class RAPLSysFSInput(GenericInput):
    max_counter_value = 2 ** 64 - 1  # Assuming a 64-bit counter for RAPL

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
        per_core_usage = psutil.cpu_percent(percpu=True, interval=None)

        for proc in psutil.process_iter(["name", "username"]):
            try:
                if "subscriber.py" in proc.cmdline():
                    self.utilization = proc.cpu_percent(interval=None)
                    proc_usage = proc.cpu_percent(interval=None) / sum(per_core_usage)
                    break
                else:
                    self.utilization = per_core_usage
                    proc_usage = 1
            except psutil.ZombieProcess:
                continue
        total_energy = self.read_energy()
        self.current_energy = self.handle_overflow(total_energy)
        self.previous_energy = total_energy
        return self.current_energy / 1000000 * proc_usage

    def handle_overflow(self, current_energy: int) -> int:
        if current_energy < self.previous_energy:
            overflow_correction = self.max_counter_value - self.previous_energy + current_energy + 1
            return overflow_correction
        else:
            return current_energy - self.previous_energy

    def get_utilization(self) -> float:
        return self.utilization