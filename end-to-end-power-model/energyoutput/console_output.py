from .generic_output import GenericOutput

class ConsoleOutput(GenericOutput):
    def report_energy(self, device: str, energy: int) -> None:
        print(f"Energy used by {device}: {energy} µJ")