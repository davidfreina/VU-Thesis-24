from .generic_input import GenericInput

# Based on:
# Yoon, Chanmin & Kim, Dongwon & Jung, Wonwoo & Kang, Chulkoo & Cha, Hojung. (2012). AppScope: Application Energy Metering Framework for Android Smartphones using Kernel Activity Monitoring. USENIX ATC.
class WiFiEstimatorInput(GenericInput):
    def __init__(self, interface: str, pps_threshold: int = 25,
                 base_low_power: float = 0.2387, base_high_power: float = 0.2470,
                 power_per_packet_low_power: float = 0.0012, power_per_packet_high_power: float = 0.008):
        super().__init__()
        self.interface = interface
        self.previous_packets = self.read_packets()
        self.threshold = pps_threshold
        self.blp = base_low_power
        self.bhp = base_high_power
        self.ppplp = power_per_packet_low_power
        self.ppphp = power_per_packet_high_power


    def __str__(self):
        return self.interface

    def read_packets(self) -> int:
        # with open(f"/sys/class/net/{self.interface}/statistics/tx_packets", 'r') as file:
        with open(f"/home/dfreina/tx_packets_simulation", 'r') as file:
            packets = int(file.read().strip())
        return packets

    def get_energy(self) -> float:
        current_packets = self.read_packets()
        packets_transmitted = current_packets - self.previous_packets
        self.previous_packets = current_packets
        print(packets_transmitted)
        # If the amount of packets transmitted in 1 second is bigger than the
        # given threshold the Wi-Fi card would switch into high power transmission mode
        # Otherwise it would use low power transmission mode
        if packets_transmitted > self.threshold:
            return self.ppphp * packets_transmitted + self.bhp
        return self.ppplp * packets_transmitted + self.blp