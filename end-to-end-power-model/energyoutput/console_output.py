from .generic_output import GenericOutput

class ConsoleOutput(GenericOutput):
    def report_power(self, device: str, current: int) -> None:
        print(f"Power used by {device}: {(current):.2f} W")

    def __str__(self):
        return "ConsoleOutput"
