"""
LE LIEN VERS LA DOC : https://openweathermap.org/current

@TODO: faire en sorte que l'utilisation du dotenv soit plus propre (et fonctionnel)


Bon, pour l'instant le fichier va etre en vrac pdt un moment, le temps que je trouve comment je vais organiser tout ca.
En gros, le principe est que ce fichier va gérer les requests vers l'API OpenWeatherMap.

Pour ca, le principe est simple, en gros on va fractionner l'url de la request en plusieurs parties (théoriquement une par argument)
et on va les concaténer pour former l'url finale.

Coté logistique, ce fichier va se contenter de faire les appels bêtement quand on lui demande.
Pour ce qui est optimisation et controle de fréquence (pour éviter un surplus d'appels), ca sera géré dans un autre fichier.
"""

import config as cfg #for env variables
import requests
import os
import json
import time
import threading
from datetime import datetime, timedelta
from loguru import logger

# Initialize the logger
logger.add("data/app.log", rotation="500 MB", level="DEBUG")

def requestBuilder(input_url: str, city: str, country: str) -> str:
    """this function is used to build the url for the request to the OpenWeatherMap API

    Args:
        input_url (str): the base URL for the API request
        city (str): the city for which we want the weather
        country (str): the country of the city

    Returns:
        str: the url for the request 
    """
    
    #internal variables
    url: str

    # building the url
    url = input_url
    url += city + "," + country
    url += "&APPID=" + cfg.WEATHER_TOKEN
    return url


def fetchWeatherData(city: str, country: str, mode: str) -> None:
    """make an API call for current weather at specified location.

    Args:
        city (str): the city from which we want the current weather
        country (str): country of the city
    """
    
    #internal variables
    base_url: str
    request_url: str
    response: requests.Response
    weather_data: dict
    now: datetime
    date_str: str
    hour_str: str
    output_file: str
    
    if (mode == "current"):
        base_url = cfg.CURRENT_WEATHER_URL
    elif (mode == "forecast"):
        base_url = cfg.HOURLY_FORECAST_URL
    else:
        logger.error("Invalid mode. Please use 'current' or 'forecast'.")
        
    # Make the API request
    request_url = requestBuilder(base_url, city, country)
    response = requests.get(request_url)
    
    """
    If data is fetched correctly, we save it in a file with the following format: date_hour_city_country_Current.json
    if not, we raise an error
    """
    if response.status_code == 200:
        weather_data = response.json()
        # Ensure the 'data' directory exists
        os.makedirs('data', exist_ok=True)

        # Get the current date and time for the file's name
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        hour_str = now.strftime("%H-%M-%S")

        # Define the path for the output file with the new format
        output_file = os.path.join('data', f"{date_str}_{hour_str}_{city}_{country}_Current.json")
        logger.info(f"Writing weather data to {output_file}")
        
        # Write the weather data to the file
        with open(output_file, 'w') as file:
            json.dump(weather_data, file, indent=4)
        
    else:
        logger.error(f"Error fetching data: {response.status_code}")

    
def houseKeeper() -> None:
    """this function files older than one hour in the data folder.
        This function MUST be run in a separate thread to avoid blocking the main program.    
    """
    #internal variables
    now: datetime
    creation_time: datetime
    data_folder: str
    file_path: str
    
    data_folder = 'data'
    
    # Check if the function is running in the main thread. If it is, log an error and return
    if not threading.current_thread().name != "MainThread":
        logger.error("This function should be run in a separate thread to avoid blocking the main program.")
        return
    
    # Loop indefinitely
    while True:
        now = datetime.now()
        for filename in os.listdir(data_folder):
            file_path = os.path.join(data_folder, filename)
            if os.path.isfile(file_path):
                creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
                if now - creation_time > timedelta(hours=1):
                    os.remove(file_path)
                    logger.info(f"Deleted old file: {file_path}")
        time.sleep(60) 


#TODO retirer ca quand on aura fini
def main():
    # Internal variables
    city: str
    country: str
    mode: str
    cleaning_thread: threading.Thread
    main_thread: threading.Thread

    def main_task():
        nonlocal city, country, mode
        city = input("Entrez la ville: ")
        country = input("Entrez le pays: ")
        mode = input("quel mode (current ou hourly): ")
        fetchWeatherData(city, country, mode)
        # TODO stacktrace affiché quand mauvais mode

    # Cleaning thread setup
    cleaning_thread = threading.Thread(target=houseKeeper)
    cleaning_thread.daemon = True  # This will make the thread close when the main program ends
    cleaning_thread.start()

    # Main thread setup
    main_thread = threading.Thread(target=main_task)
    main_thread.start()
    main_thread.join()  # Wait for the main thread to finish

if __name__ == "__main__":
    main()