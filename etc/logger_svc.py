import sys
import logging
from logging.handlers import RotatingFileHandler
import queue
from logging.handlers import QueueListener, QueueHandler

DEFAULT_LOGGING_FILE = "logs/logger.txt"


class CustomLogger:
    def __init__(self, module, config):
        self.que = queue.Queue(-1)
        self.queue_handler = QueueHandler(self.que)
        self.log_filename = config.get("logging_file", DEFAULT_LOGGING_FILE)
        self.log_level = config.get("logging_level".upper(), "DEBUG")

        self.logger = logging.getLogger(module)
        self.logger.setLevel(self.log_level)
        self.formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s " "- %(message)s"
        )
        self.console_handler = logging.StreamHandler(sys.stdout)
        self.file_handler = RotatingFileHandler(self.log_filename,
                                                maxBytes=config.get("log_max_size", 4096),
                                                backupCount=config.get("backup_count", 2))
        self.console_handler.setFormatter(self.formatter)
        self.file_handler.setFormatter(self.formatter)
        self.listener = QueueListener(self.que, self.console_handler, self.file_handler)

        self.logger.addHandler(self.queue_handler)
        self.listener.start()

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)