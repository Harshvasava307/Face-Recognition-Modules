# database_module.py

import os
import csv
from datetime import datetime


class FaceDatabaseLogger:
    def __init__(self, log_file="recognized_faces.csv"):
        self.log_file = log_file
        # Create CSV file with headers if it doesn't exist
        if not os.path.exists(self.log_file):
            with open(self.log_file, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Name", "Date", "Time"])

    def log_recognition(self, name):
        """
        Log a recognized face with timestamp.
        """
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        with open(self.log_file, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([name, date_str, time_str])
        print(f"Logged {name} at {date_str} {time_str}")


# ------------------- Test Code -------------------
if __name__ == "__main__":
    logger = FaceDatabaseLogger()

    # Example: log a recognized face
    logger.log_recognition("Harsh")
    logger.log_recognition("Shiv")
