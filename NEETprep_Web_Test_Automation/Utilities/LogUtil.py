import logging
import os
import time

# <project>/Logs, independent of the current working directory and OS
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Logs")


class Logger():

    def __init__(self, logger, file_level=logging.INFO):
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        fmt = logging.Formatter('%(asctime)s - %(filename)s:[%(lineno)s] - [%(levelname)s] - %(message)s')

        curr_time = time.strftime("%Y-%m-%d")
        os.makedirs(LOG_DIR, exist_ok=True)
        self.LogFileName = os.path.join(LOG_DIR, 'log' + curr_time + '.txt')
        if self.logger.handlers:  # already configured; avoid duplicate log lines
            return
        # "a" to append the logs in same file, "w" to generate new logs and delete old one
        fh = logging.FileHandler(self.LogFileName, mode="a")
        fh.setFormatter(fmt)
        fh.setLevel(file_level)
        self.logger.addHandler(fh)

