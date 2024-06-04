from .generic_input import GenericInput

class NetworkPacketInput(GenericInput):
    def __init__(self, interface: str, energy_per_packet: float):
        super().__init__()
        self.interface = interface
        self.energy_per_packet = energy_per_packet
        self.previous_packets = self.read_packets()

    def __str__(self):
        return self.interface

    def read_packets(self) -> int:
        with open(f"/sys/class/net/{self.interface}/statistics/tx_packets", 'r') as file:
            packets = int(file.read().strip())
        return packets

    def read_energy(self) -> float:
        current_packets = self.read_packets()
        packets_transmitted = current_packets - self.previous_packets
        self.previous_packets = current_packets
        return packets_transmitted * self.energy_per_packet
