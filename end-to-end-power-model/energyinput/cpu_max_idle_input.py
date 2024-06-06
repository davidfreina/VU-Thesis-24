import os

from .generic_input import GenericInput


class CPUMaxIdleInput(GenericInput):
    def __init__(self, p_max: float, p_idle: float):
        self.p_max = p_max
        self.p_idle = p_idle
        self.previous_usage = self.get_cpu_usage()
        self.previous_energy = self.read_energy()
        self.cpu_cores = os.cpu_count()

    def read_energy(self) -> int:
        usage = {}
        for cpu_id, current_times in self.get_cpu_usage().items():
            prev_times = self.previous_usage[cpu_id]
            total_diff = sum(current_times) - sum(prev_times)
            idle_diff = current_times[3] - prev_times[3]
            usage[cpu_id] = 100 * (total_diff - idle_diff) / total_diff
        print(usage)
        return 0

    def get_cpu_usage(self) -> dict:
        with open("/proc/stat", "r") as file:
            lines = file.readlines()

        cpu_data = {}
        for line in lines:
            if line.startswith("cpu"):
                parts = line.split()
                cpu_id = parts[0]
                cpu_data[cpu_id] = self.parse_cpu_line(line)
        return cpu_data

    def parse_cpu_line(self, line) -> list:
        parts = line.split()
        times = list(map(int, parts[1:]))
        return times
