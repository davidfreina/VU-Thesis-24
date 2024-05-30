from .generic_output import GenericOutput

class ConsoleOutput(GenericOutput):
    def report_energy(self, device: str, current: int, energy: int) -> None:
        print(f"Energy used by {device}: {current} µJ, total since start: {energy} µJ")