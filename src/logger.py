import csv
import datetime

class DataLogger:
    def __init__(self, filename):
        self.filename = filename
        # Create the CSV file and write the header if it doesn't exist
        self._initialize_csv()

    def _initialize_csv(self):
        try:
            with open(self.filename, mode='x', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'Pattern Type', 'Detected Color', 'Additional Info'])
        except FileExistsError:
            pass  # File already exists, no need to write header again

    def log_data(self, pattern_type, detected_color, additional_info=''):
        timestamp = datetime.datetime.now().isoformat()
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, pattern_type, detected_color, additional_info])

# Example usage
if __name__ == "__main__":
    logger = DataLogger('data_log.csv')
    logger.log_data('Stripe', 'Red', 'Detected during daytime')
    logger.log_data('Solid', 'Blue', 'Detected at night')
