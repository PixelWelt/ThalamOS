"""global logger configuration
This module configures a global logger using the Loguru library.
The logger is set up to write log messages to 'storagemanager.log' with the following specifications:
- Log message format: "{time} {level} {message}"
- Log level: INFO
- Log file rotation: 10 MB
- Log file compression: zip
- Log file retention: 2 days
Usage:
    logger.info("This is an info message")
    logger.error("This is an error message")
"""
from loguru import logger

logger.add("storagemanager.log",
           format="{time} {level} {message}",
           level="INFO",
           rotation="10 MB",
           compression="zip",
           retention="2 days")
