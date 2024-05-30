from abc import ABC, abstractmethod
from energyinput.rapl_sysfs_input import RAPLSysFSInput
from energyinput.network_packet_input import NetworkPacketInput
from energyoutput.generic_output import GenericOutput
from energyoutput.console_output import ConsoleOutput
import time
import os

class EndToEndPowerModel():
    def __init__(self, input_sources: dict, output_destination: GenericOutput):
        self.input_sources = input_sources
        self.output_destination = output_destination
        self.last_energy = {device: input_source.read_energy() for device, input_source in input_sources.items()}
        self.total_energy = {device: 0 for device in input_sources}

    def handle_overflow(self, current_energy: int, last_energy: int) -> int:
        if current_energy < last_energy:
            max_counter_value = 2**32 - 1  # Assuming a 32-bit counter for RAPL
            overflow_correction = max_counter_value - last_energy + current_energy + 1
            return overflow_correction
        else:
            return current_energy - last_energy

    def monitor_energy(self):
        while True:
            current_energies = {device: input_source.read_energy() for device, input_source in self.input_sources.items()}
            for device, current_energy in current_energies.items():
                energy_used = self.handle_overflow(current_energy, self.last_energy[device])
                self.total_energy[device] += energy_used
                self.last_energy[device] = current_energy
                self.output_destination.report_energy(device, self.total_energy[device])
            time.sleep(1)

if __name__ == "__main__":
    rapl_file_path = "/sys/class/powercap/intel-rapl:0/energy_uj"
    network_interfaces = ["eno0", "eno1"]
    energy_per_packet = 10  # Energy per packet in µJ (example value)

    energy_input_rapl = RAPLSysFSInput(rapl_file_path)
    energy_inputs_network = {iface: NetworkPacketInput(iface, energy_per_packet) for iface in network_interfaces}
    energy_inputs = {"RAPL": energy_input_rapl, **energy_inputs_network}

    energy_output = ConsoleOutput()

    monitor = EndToEndPowerModel(energy_inputs, energy_output)
    monitor.monitor_energy()