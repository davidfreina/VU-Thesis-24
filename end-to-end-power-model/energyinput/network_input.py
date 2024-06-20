from typing import Tuple

from .generic_input import GenericInput

class NetworkInput(GenericInput):
    def __init__(self, interface: str, model: str):
        super().__init__()
        self.interface = interface
        self.previous_up_packets, self.previous_down_packets = self.read_packets()
        self.previous_up_bytes, self.previous_down_bytes = self.read_bytes()
        self.utilization_bytes = 0
        self.utilization_packets = 0
        self.model = model

    def __str__(self):
        return self.interface

    def read_packets(self) -> Tuple[int, int]:
        with open(f"/sys/class/net/{self.interface}/statistics/tx_packets", 'r') as file:
            packets_up = int(file.read().strip())
        with open(f"/sys/class/net/{self.interface}/statistics/rx_packets", 'r') as file:
            packets_down = int(file.read().strip())
        return packets_up, packets_down

    def read_bytes(self) -> Tuple[int, int]:
        with open(f"/sys/class/net/{self.interface}/statistics/tx_bytes", 'r') as file:
            curr_up_bytes = int(file.read().strip())
        with open(f"/sys/class/net/{self.interface}/statistics/rx_bytes", 'r') as file:
            curr_down_bytes = int(file.read().strip())
        return curr_up_bytes, curr_down_bytes


    def get_energy(self) -> float:
        if self.model == "ardito2018":
            current_up_bytes, current_down_bytes = self.read_bytes()
            bw_up_mbps = (current_up_bytes - self.previous_up_bytes) / 1048576
            bw_down_mpbs = (current_down_bytes - self.previous_down_bytes) / 1048576
            self.utilization_bytes = bw_up_mbps + bw_down_mpbs
            self.previous_up_bytes = current_up_bytes
            self.previous_down_bytes = current_down_bytes
            if bw_up_mbps <= 41.2:
                p_idle_up = 1.613
                e_up = 0.00164 * bw_up_mbps
            else:
                p_idle_up = 1.685
                e_up = 0.00182 * bw_up_mbps
            if bw_down_mpbs <= 42.5:
                p_idle_down = 1.654
                e_down = 0.00162 * bw_down_mpbs
            else:
                p_idle_down = 1.728
                e_down = 0.00210 * bw_down_mpbs
            return e_up + e_down + (p_idle_up + p_idle_down) / 2
        if self.model == "reviriego2011":
            # According to Reviriego, P., K. Christensen, J. Rabanillo, and J. A. Maestro. ‘An Initial Evaluation of Energy Efficient Ethernet’. IEEE Communications Letters 15, no. 5 (May 2011): 578–80. https://doi.org/10.1109/LCOMM.2011.040111.102259.
            # No Traffic on the NIC uses 525mW
            # 5000 250 byte packets per second use 531mW
            # Therefore, one packet approximately uses 0,0012mW of power
            power_per_packet = 0.0000012  # Power per packet in W
            current_up_packets, current_down_packets = self.read_packets()
            packets_up = current_up_packets - self.previous_up_packets
            packets_down = current_down_packets - self.previous_down_packets
            self.utilization_packets = packets_up + packets_down
            self.previous_up_packets = current_up_packets
            self.previous_down_packets = current_down_packets
            return (packets_up + packets_down) * power_per_packet + 0.525

    def get_utilization(self) -> float:
        if self.model == "ardito2018":
            return self.utilization_bytes
        elif self.model == "reviriego2011":
            return self.utilization_packets
