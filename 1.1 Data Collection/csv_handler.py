import csv
import os


class CSVWriter:
    def __init__(self, filename, headers):
        """
        Initialize the CSVWriter instance.

        Parameters:
        - filename: The name of the CSV file to write to.
        - headers: The list of headers for the CSV file.
        """
        self.filename = filename
        self.headers = headers
        self.buffer = []  # Buffer to temporarily store rows before writing
        self.file = None  # File object for the CSV file
        self.writer = None  # CSV writer object
        self.file_exists = os.path.exists(filename)  # Check if the file already exists

    def initialize(self):
        """
        Initialize the CSV file for writing.

        Opens the file in append mode if it already exists; otherwise, opens it in write mode.
        Writes the headers to the file if it does not already exist.
        """
        mode = "a" if self.file_exists else "w"
        self.file = open(self.filename, mode=mode, encoding="utf-8", newline="")
        self.writer = csv.writer(self.file)
        if not self.file_exists:
            self.writer.writerow(self.headers)  # Write headers if the file is new
            self.file_exists = True

    def write_row(self, row_data):
        """
        Write a single row of data to the CSV file.

        Parameters:
        - row_data: List of data values corresponding to the CSV headers.

        The row is added to a buffer and flushed to the file when the buffer reaches a size of 12.
        """
        self.buffer.append(row_data)
        if len(self.buffer) >= 12:
            self.flush_buffer()  # Flush the buffer to the file if it has 12 or more rows

    def flush_buffer(self):
        """
        Flush the buffer by writing all buffered rows to the CSV file.

        Only non-empty rows are written to the file.
        """
        for row in self.buffer:
            if any(row):  # Check if the row is not entirely empty
                self.writer.writerow(row)
        self.buffer = []  # Clear the buffer after flushing
        self.file.flush()  # Ensure all data is written to the file

    def close(self):
        """
        Close the CSV file.

        Flushes any remaining rows in the buffer and closes the file object.
        """
        if self.file:
            self.flush_buffer()  # Ensure any remaining buffered rows are written
            self.file.close()  # Close the file object


def initialize_csv_writer(filename, headers):
    """
    Factory function to create and return a CSVWriter instance.

    Parameters:
    - filename: The name of the CSV file to write to.
    - headers: The list of headers for the CSV file.

    Returns:
    A CSVWriter instance initialized with the provided filename and headers.
    """
    return CSVWriter(filename, headers)
