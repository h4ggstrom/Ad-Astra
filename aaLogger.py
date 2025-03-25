"""
This file is used to configure the logger for the Ad-Astra project.
"""

from loguru import logger

logger.add("utils/Ad-Astra.log", rotation="500 MB", level="DEBUG")