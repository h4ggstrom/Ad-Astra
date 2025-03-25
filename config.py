# Description: This file is used to centralize the variables that are used in the bot.
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
GEOLOC_URL = os.getenv('GEOLOC_URL')