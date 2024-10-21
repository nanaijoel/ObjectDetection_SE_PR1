# Logger class, handles creating a document and writing logs in there

import csv
import datetime
import os


class DataLogger:
    def __init__(self, config, mode):
        log_file = os.path.join(config['DEFAULT']['log_folder'], 'data_log.csv')
        self.mode = mode
        if self.mode == 'CAMERA':
            self.log_interval = float(config['CAMERA']['log_interval'])
        else:
            self.log_interval = None
        self.filename = log_file
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
        if self.mode == 'CAMERA':
            if self.last_log_time is None or (current_time - self.last_log_time).total_seconds() >= self.log_interval:
                with open(self.filename, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([current_time.isoformat(), shape, color])
                self.last_log_time = current_time
        else:
            with open(self.filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([current_time.isoformat(), shape, color])
