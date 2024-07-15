import sys
from abc import ABC, abstractmethod
from energyinput.rapl_sysfs_input import RAPLSysFSInput
from energyinput.rapl_sysfs_mem_input import RAPLSysFSMemInput
from energyinput.network_input import NetworkInput
from energyinput.cpu_max_idle_input import CPUMaxIdleInput
from energyinput.wifi_estimator_input import WiFiEstimatorInput
from energyinput.camera_input import CameraInput
from energyoutput.generic_output import GenericOutput
from energyoutput.console_output import ConsoleOutput
from energyoutput.csv_output import CsvOutput
import time
import os
import argparse

class EndToEndPowerModel():
    def __init__(self, input_sources: dict, output_destinations: list):
        self.input_sources = input_sources
        self.output_destinations = output_destinations
        self.total_energy = {device: 0 for device in input_sources}
        self.current_energy = {device: input_source.get_energy() for device, input_source in self.input_sources.items()}

    def monitor_energy(self):
        counter = 1
        while True:
            current_values = {input_source: [input_source.get_energy(), input_source.get_utilization()] for device, input_source in self.input_sources.items()}
            for device, current in current_values.items():
                self.total_energy[str(device)] += current[0]
                self.current_energy[str(device)] = current[0]
                for output in self.output_destinations:
                    if str(output) == "ConsoleOutput":
                        output.report_power(str(device), self.current_energy[str(device)])
            for output in self.output_destinations:
                if str(output) == "CsvOutput":
                    output.report_power(current_values)
            counter += 1
            time.sleep(1)


def handle_endpoint():
    energy_input_wifi = WiFiEstimatorInput("ens2", 20, 0.110, 0.1407, 0.002, 0.007)
    energy_input_cpu = CPUMaxIdleInput(p_base=0.190, model="yoon2017")
    energy_input_camera = CameraInput()
    energy_inputs = {str(energy_input_camera): energy_input_camera, str(energy_input_wifi): energy_input_wifi, str(energy_input_cpu): energy_input_cpu}

    energy_output = ConsoleOutput()
    csv_output = CsvOutput("endpoint.csv")

    monitor = EndToEndPowerModel(energy_inputs, [energy_output, csv_output])
    monitor.monitor_energy()


def handle_edge():
    energy_input_cpu = CPUMaxIdleInput(p_base=1.488, model="kaup2018")
    energy_input_network = NetworkInput("ens2", "ardito2018")
    energy_inputs = {str(energy_input_network): energy_input_network, str(energy_input_cpu): energy_input_cpu}
    energy_output = ConsoleOutput()
    csv_output = CsvOutput("edge.csv")

    monitor = EndToEndPowerModel(energy_inputs, [energy_output, csv_output])
    monitor.monitor_energy()
    pass


def handle_cloud():
    rapl_paths = ["/sys/class/powercap/intel-rapl:0/energy_uj", "/sys/class/powercap/intel-rapl:1/energy_uj"]
    rapl_mem_paths = ["/sys/class/powercap/intel-rapl:0:0/energy_uj", "/sys/class/powercap/intel-rapl:1:0/energy_uj"]
    network_interfaces = ["eno1"]

    energy_input_rapl_cpu = RAPLSysFSInput(rapl_paths)
    energy_inputs_rapl_mem = {path.split('/').pop(-2): RAPLSysFSMemInput(path) for path in rapl_mem_paths}
    energy_inputs_network = {iface: NetworkInput(iface, "reviriego2011") for iface in network_interfaces}
    energy_inputs = {str(energy_input_rapl_cpu): energy_input_rapl_cpu, **energy_inputs_rapl_mem, **energy_inputs_network}

    energy_output = ConsoleOutput()
    csv_output = CsvOutput("cloud.csv")

    monitor = EndToEndPowerModel(energy_inputs, [energy_output, csv_output])
    monitor.monitor_energy()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process command line parameters")
    parser.add_argument('layer', choices=['endpoint', 'edge', 'cloud'], help="Specify the layer to measure")

    args = parser.parse_args()

    if args.layer == 'endpoint':
        handle_endpoint()
    elif args.layer == 'edge':
        handle_edge()
    elif args.layer == 'cloud':
        handle_cloud()

