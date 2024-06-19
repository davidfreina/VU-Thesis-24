import psutil

from .generic_input import GenericInput

class CPUMaxIdleInput(GenericInput):
    def __init__(self, p_max: float = 0, p_idle: float = 0, p_base: float = 0, model: str = "basmadjian2011"):
        super().__init__()
        self.p_max = p_max
        self.p_idle = p_idle
        self.p_base = p_base
        self.model = model
        self.coefficient = 0
        self.previous_energy = self.get_energy()

    def __str__(self):
        return "CPUMaxIdleModel"

    def get_energy(self) -> float:
        per_core_usage = psutil.cpu_percent(percpu=True, interval=None)
        # https://doi.org/10.1145/1250662.1250665
        if self.model == "fan2007":
            return self.p_idle + (self.p_max - self.p_idle) * per_core_usage[0]
        # https://doi.org/10.1145/2318716.2318718
        elif self.model == "basmadjian2011":
            per_core_energy_max = [usage * self.p_max for usage in per_core_usage]
            return self.p_idle * sum(per_core_energy_max)
        # https://doi.org/10.1016/j.sysarc.2017.10.001
        elif self.model == "yoon2017":
            if len(per_core_usage) == 1:
                self.p_idle = 0.26 - self.p_base
                self.coefficient = 2.333
            elif len(per_core_usage) == 2:
                self.p_idle = 0.35 - self.p_base
                self.coefficient = 5.4
            elif len(per_core_usage) == 3:
                self.p_idle = 0.39 - self.p_base
                self.coefficient = 8
            elif len(per_core_usage) == 4:
                self.p_idle = 0.5 - self.p_base
                self.coefficient = 10.25
            else:
                self.logger.error("This model only works for CPUs with 1-4 cores!")
                self.p_base = 0
            per_core_energy = [self.coefficient * usage + self.p_idle + self.p_base for usage in per_core_usage]
            return sum(per_core_energy)
        elif self.model == "kaup2018":
            utilization = sum(per_core_usage) / psutil.cpu_count() / 100
            return self.p_base + 0.6191 * utilization
