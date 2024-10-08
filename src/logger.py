import csv
import datetime
import time


class DataLogger:
    def __init__(self, filename, log_interval=0.5):
        self.filename = filename
        self.log_interval = log_interval
        self.last_logged = {}
        self._initialize_csv()

    def _initialize_csv(self):
        try:
            with open(self.filename, mode='x', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'Pattern Type', 'Detected Color', 'Additional Info'])
        except FileExistsError:
            pass

    def log_data(self, pattern_type, detected_color, additional_info=''):
        current_time = time.time()
        key = (pattern_type, detected_color)

        if key not in self.last_logged or (current_time - self.last_logged[key]) > self.log_interval:
            timestamp = datetime.datetime.now().isoformat()
            with open(self.filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([timestamp, pattern_type, detected_color, additional_info])
            self.last_logged[key] = current_time
