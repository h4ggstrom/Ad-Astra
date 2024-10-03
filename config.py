""" 
TODO: supp le comm quand on aura fini le fichier

Ce fichier va centraliser les tokens, et les variables du dotenv, pour éviter d'avoir à load la librairie à chaque fois qu'on en a besoin.
Donc pas un gros fichier, mais un fichier utile.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Centralize variables from .env
# the tokens
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
WEATHER_TOKEN = os.getenv('WEATHER_TOKEN')

# the urls
CURRENT_WEATHER_URL = os.getenv('CURRENT_WEATHER_URL')
HOURLY_FORECAST_URL = os.getenv('HOURLY_FORECAST_URL')
GEOLOC_URL = os.getenv('GELOC_URL')