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
        self.cpu_usage = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.cpu_usage_active = [0, 0, 0]
        self.process_usage = {}

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
        pids = []
        for proc in psutil.process_iter(["name", "username"]):
            try:
                if "subscriber.py" in proc.cmdline():
                    proc_usage += proc.cpu_percent(interval=None)
                    pids.append(proc.pid)
                    self.utilization = proc_usage
            except psutil.ZombieProcess:
                continue
            except psutil.NoSuchProcess:
                continue
        with open(f"/proc/stat", 'r') as file:
            line = file.readline().strip().split(' ')
            print(line)
            total = [int(cpu) for cpu in line[2:9]]
            total_active = [int(cpu) for cpu in line[2:5]]
            diff = sum(total) - sum(self.cpu_usage)
            diff_active = sum(total_active) - sum(self.cpu_usage_active)
            idle = total[3] - self.cpu_usage[3]
            print(total)
            use = diff - idle
            use_active = diff_active - idle
            # print(100 * use / diff)
            self.cpu_usage = total

        total_process = 0
        for pid in pids:
            with open(f"/proc/{pid}/stat", 'r') as file:
                process = sum([int(cpu) for cpu in file.readline().strip().split(' ')[13:15]])
                try:
                    process_diff = process - self.process_usage[pid]
                    self.process_usage[pid] = process
                except KeyError:
                    process_diff = 0
                    self.process_usage[pid] = process
                total_process += process_diff

        print(use)
        print(use_active)
        print(total_process)

        energies = self.read_energy()
        current_energy = 0
        for idx, energy in enumerate(energies):
            current_energy += self.handle_overflow(energy, idx)
        self.previous_energy = energies
        print(f'current: {current_energy / 1000000}')
        return current_energy / 1000000 * (total_process / use)

    def handle_overflow(self, current_energy: int, index: int) -> int:
        if current_energy < self.previous_energy[index]:
            overflow_correction = self.max_counter_value - self.previous_energy[index] + current_energy + 1
            return overflow_correction
        else:
            return current_energy - self.previous_energy[index]

    def get_utilization(self) -> float:
        return self.utilization
