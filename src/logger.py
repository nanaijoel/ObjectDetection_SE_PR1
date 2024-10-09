import csv
import datetime
import os


class DataLogger:
    def __init__(self, config):
        log_file = os.path.join(config['DEFAULT']['log_folder'], 'data_log.csv')
        log_interval = float(config['DEFAULT']['log_interval'])
        self.filename = log_file
        self.log_interval = log_interval
        self.last_log_time = None
        self._initialize_csv()

    def _initialize_csv(self):
        try:
            with open(self.filename, mode='x', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'Shape', 'Color'])
        except FileExistsError:
            pass

    def log_data(self, shape, color):
        current_time = datetime.datetime.now()
        if self.last_log_time is None or (current_time - self.last_log_time).total_seconds() >= self.log_interval:
            with open(self.filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([current_time.isoformat(), shape, color])
            self.last_log_time = current_time
