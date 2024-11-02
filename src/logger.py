# Logger class, handles creating a document and writing logs in there

import csv
import datetime
import os


class DataLogger:
    def __init__(self, config, mode):
        log_file = os.path.join(config['DEFAULT']['log_folder'], 'data_log.csv')
        self.filename = log_file
        self._initialize_csv()
        self.mode = mode
        if self.mode == 'CAMERA' or self.mode == 'GUI':
            self.log_interval = float(config['CAMERA']['log_interval'])
        else:
            self.log_interval = None
        self.last_logged_time = None
        self.selected_shape = None

    def _initialize_csv(self):
        try:
            with open(self.filename, mode='x', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'Shape', 'Color'])
        except FileExistsError:
            pass


    def log_shapes(self, shapes):
        """
        Writes shape parameters to logfile with actual timestamp
        :param string describing the shape
        """
        current_time = datetime.datetime.now()
        if self.last_logged_time is None:
            self.last_logged_time = current_time

        if (self.log_interval is None or (current_time - self.last_logged_time).total_seconds()
                >= self.log_interval):
            self.last_logged_time = current_time
            for contour, shape, color_name in shapes:
                if self.selected_shape is None or shape == self.selected_shape:
                    self.log_data(shape, color_name)


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
