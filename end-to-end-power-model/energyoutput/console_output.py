from .generic_output import GenericOutput

class ConsoleOutput(GenericOutput):
    def report_power(self, device: str, current: int, energy: int) -> None:
        print(f"Power used by {device}: {(current):.1f} W, sum since start: {(energy):.1f} W")