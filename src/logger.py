# Logger class, handles creating a document and writing logs in there

import csv
import datetime
import os


class DataLogger:
    def __init__(self, config):
        log_file = os.path.join(config['DEFAULT']['log_folder'], 'data_log.csv')
        self.filename = log_file
        self._initialize_csv()

    def _initialize_csv(self):
        try:
            with open(self.filename, mode='x', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'Shape', 'Color'])
        except FileExistsError:
            pass

    def log_data(self, shape, color):
        """
        Writes given parameters to logfile with actual timestamp
        :shape: string describing the shape
        :color: string describing the color
        """
        current_time = datetime.datetime.now()
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([current_time.isoformat(), shape, color])

