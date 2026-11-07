"""
LogUtil - file logger used by the Page Objects.

Usage:
    log = Logger(__name__, logging.INFO)
    log.logger.info("Step: Clicking on ...")

Output:
    Logs/log<YYYY-MM-DD>.txt (one file per day, appended). The Logs folder is git-ignored.
    Console output is configured separately in pytest.ini (log_cli).
"""
import logging
import os
import time

# <project>/Logs, independent of the current working directory and OS
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Logs")


class Logger():

    def __init__(self, logger, file_level=logging.INFO):
        # Get (or create) a named logger, usually the module name
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        # Log line format: time - file:[line] - [LEVEL] - message
        fmt = logging.Formatter('%(asctime)s - %(filename)s:[%(lineno)s] - [%(levelname)s] - %(message)s')

        # Daily log file name, e.g. Logs/log2026-11-07.txt
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

