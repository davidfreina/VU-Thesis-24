from .generic_input import GenericInput
from typing import Tuple

# Based on:
# Yoon, Chanmin & Kim, Dongwon & Jung, Wonwoo & Kang, Chulkoo & Cha, Hojung. (2012). AppScope: Application Energy Metering Framework for Android Smartphones using Kernel Activity Monitoring. USENIX ATC.
class WiFiEstimatorInput(GenericInput):
    def __init__(self, interface: str, pps_threshold: int = 25,
                 base_low_power: float = 0.2387, base_high_power: float = 0.2470,
                 power_per_packet_low_power: float = 0.0012, power_per_packet_high_power: float = 0.008):
        super().__init__()
        self.interface = interface
        self.previous_packets_up, self.previous_packets_down = self.read_packets()
        self.threshold = pps_threshold
        self.blp = base_low_power
        self.bhp = base_high_power
        self.ppplp = power_per_packet_low_power
        self.ppphp = power_per_packet_high_power
        self.utilization = 0


    def __str__(self):
        return self.interface

    def read_packets(self) -> Tuple[int, int]:
        with open(f"/sys/class/net/{self.interface}/statistics/tx_packets", 'r') as file:
            packets_up = int(file.read().strip())
        with open(f"/sys/class/net/{self.interface}/statistics/rx_packets", 'r') as file:
            packets_down = int(file.read().strip())
        return packets_up, packets_down

    def get_energy(self) -> float:
        current_packets_up, current_packets_down = self.read_packets()
        packets_up = current_packets_up - self.previous_packets_up
        packets_down = current_packets_down - self.previous_packets_down
        self.utilization = packets_up + packets_down
        self.previous_packets_up = current_packets_up
        self.previous_packets_down = current_packets_down
        # If the amount of packets transmitted in 1 second is bigger than the
        # given threshold the Wi-Fi card would switch into high power transmission mode
        # Otherwise it would use low power transmission mode
        if (packets_up + packets_down) > self.threshold:
            return self.ppphp * (packets_up + packets_down) + self.bhp
        return self.ppplp * (packets_up + packets_down) + self.blp

    def get_utilization(self) -> float:
        return self.utilization
