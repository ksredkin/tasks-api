import logging
from tasks_api.core.config import LOGS_PATH
import os

class Logger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.setup_logger()
        
    def setup_logger(self):
        if not os.path.exists(LOGS_PATH):
            os.mkdir(LOGS_PATH)

        file_handler = logging.FileHandler(f"{LOGS_PATH}{self.logger.name}.log", "w", encoding="utf-8")
        stream_handler = logging.StreamHandler()

        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

    def get_logger(self):
        return self.logger