""" 
Ce fichier sert à centraliser le logger, pour éviter de devoir le réimporter et reconfigurer les paramètres dans chaque fichier.
"""

from loguru import logger

logger.add("utils/Ad-Astra.log", rotation="500 MB", level="DEBUG")