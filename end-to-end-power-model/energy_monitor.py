import sys
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
        self.total_energy = {device: 0 for device in input_sources}
        self.current_energy = {device: input_source.get_energy() for device, input_source in self.input_sources.items()}

    def monitor_energy(self):
        counter = 1
        while True:
            current_energies = {input_source: input_source.get_energy() for device, input_source in self.input_sources.items()}
            for device, current_energy in current_energies.items():
                self.total_energy[str(device)] += current_energy
                self.current_energy[str(device)] = current_energy
                self.output_destination.report_power(device, self.current_energy[str(device)], self.total_energy[str(device)])
                print(f"Energy used by {device}: {(self.total_energy[str(device)] / counter * (counter / 60 / 60)):.1f} Wh")
            counter += 1
            time.sleep(1)

if __name__ == "__main__":
    rapl_file_path = "/sys/class/powercap/intel-rapl:0/energy_uj"
    network_interfaces = ["eno1", "eno2"]
    # According to Reviriego, P., K. Christensen, J. Rabanillo, and J. A. Maestro. ‘An Initial Evaluation of Energy Efficient Ethernet’. IEEE Communications Letters 15, no. 5 (May 2011): 578–80. https://doi.org/10.1109/LCOMM.2011.040111.102259.
    # No Traffic on the NIC uses 525mW
    # 5000 250 byte packets per second use 531mW
    # Therefore, one packet approximately uses 0,0012mW of power
    power_per_packet = 0.0000012  # Power per packet in W

    energy_input_rapl = RAPLSysFSInput(rapl_file_path)
    energy_inputs_network = {iface: NetworkPacketInput(iface, power_per_packet) for iface in network_interfaces}
    energy_inputs = {str(energy_input_rapl): energy_input_rapl, **energy_inputs_network}

    energy_output = ConsoleOutput()

    monitor = EndToEndPowerModel(energy_inputs, energy_output)

    monitor.monitor_energy()
