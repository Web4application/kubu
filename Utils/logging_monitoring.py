# Example: utils/logging_monitoring.py
import logging

def setup_logging(log_file):
    """
    Set up logging configuration.

    Parameters:
    log_file (str): Path to the log file.
    """
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def log_message(message):
    """
    Log a message.

    Parameters:
    message (str): Message to log.
    """
    logging.info(message)

# Example usage
if __name__ == "__main__":
    setup_logging('path/to/log_file.log')
    log_message('This is a log message.')
