from .generic_output import GenericOutput
import time
import os
import csv

class CsvOutput(GenericOutput):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = {}  # Store the current power data for multiple devices

    def __str__(self):
        return "CsvOutput"

    def report_power(self, power: dict) -> None:
        timestamp = int(time.time())
        if timestamp not in self.data:
            self.data[timestamp] = {}
        for device, power in power.items():
            self.data[timestamp][str(device)] = power[0]
            self.data[timestamp][f'{device} Utilization'] = power[1]
        self.save_to_csv()
        self.data = {}

    def save_to_csv(self):
        headers = ['Timestamp']
        rows = []

        # Collect all unique device names as headers
        for timestamp, devices in self.data.items():
            for device in devices.keys():
                if device not in headers:
                    headers.append(device)

        # Collect the rows of data
        for timestamp, devices in self.data.items():
            row = [timestamp]
            for header in headers[1:]:
                if header in devices:
                    row.append(devices[header])
                else:
                    row.append('')
            rows.append(row)

        file_exists = os.path.isfile(self.file_path)

        with open(self.file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(headers)
            writer.writerows(rows)
