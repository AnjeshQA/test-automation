"""
configReader - reads values from ConfigurationData/conf.ini.

Usage:
    from Utilities import configReader
    url = configReader.readConfig("common info", "url")
    timeout = configReader.readConfig("playwright", "default_timeout_ms")

Used by BasePage (locators), conftest.py (timeouts) and the step definitions (URLs, product name).
Keys are case-insensitive (configparser lower-cases them).
"""
import os
from configparser import ConfigParser


def readConfig(section, key):
    config = ConfigParser()

    # This creates an absolute path regardless of where you run the test from
    # It goes up one level from Utilities and into ConfigurationData
    current_dir = os.path.dirname(__file__)
    path = os.path.join(current_dir, "..", "ConfigurationData", "conf.ini")

    # Fail fast with a clear message if the config file is missing
    if not os.path.exists(path):
        raise FileNotFoundError(f"Could not find conf.ini at {path}")

    # Parse the file and return the value (raises NoOptionError if the key is missing)
    config.read(path)
    return config.get(section, key)
