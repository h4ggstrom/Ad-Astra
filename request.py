"""
LE LIEN VERS LA DOC : https://openweathermap.org/current


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
logger.add("utils/Ad-Astra.log", rotation="500 MB", level="DEBUG")

def requestBuilder(input_url: str, city: str, country: str, cplt: str = "") -> str:
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
    url += cplt
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
    cplt: str
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
        cplt = "&cnt=12"
    else:
        logger.error("Invalid mode. Please use 'current' or 'forecast'.")
        return
        
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
        output_file = os.path.join('data', f"{date_str}_{hour_str}_{city}_{country}_{mode}.json")
        logger.info(f"{mode} for {city} request data saved in {output_file}")
        
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
        

def forecastFetch(json: str) -> list:
    """this function is used to extract the relevant informations from the json file containing the forecast data

    Args:
        json (str): the json file path

    Returns:
        list: the list containing the relevant informations
    """
    
    #internal variables
    data: dict
    dt: int
    humidity: int
    temp: float
    feels_like: float
    weather: str
    cloudiness: int
    wind_speed: float
    pop: float
    weather_info: dict
    info_list: list
    
    try:
        with open(json, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        logger.error(f"File not found: {json}")
        return []
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from file: {json}")
        return []
        
    info_list = []
    
    for i in data['list']:
        dt = i['dt']
        humidity = i['main']['humidity']
        temp = i['main']['temp']
        feels_like = i['main']['feels_like']
        weather = i['weather'][0]['description']
        cloudiness = i['clouds']['all']
        wind_speed = i['wind']['speed']
        pop = i['pop']

        weather_info = {
            'dt': dt,
            'humidity': humidity,
            'temp': temp,
            'feels_like': feels_like,
            'weather': weather,
            'cloudiness': cloudiness,
            'wind_speed': wind_speed,
            'pop': pop
        }
        
        info_list.append(weather_info)
        
    return info_list


#TODO: trier les infos qu'on récupère, plutot que return tout le JSON
def geoLoc(city: str, country: str) -> dict:
    """this function is used to get the geolocation of a city

    Args:
        city (str): the city for which we want the geolocation
        country (str): the country of the city

    Returns:
        dict: the dictionary containing the geolocation
    """
    
    #internal variables
    base_url: str
    request_url: str
    response: requests.Response
    geo_data: dict
    
    base_url = cfg.GEOLOC_URL
    request_url = requestBuilder(base_url, city, country)
    response = requests.get(request_url)
    
    if response.status_code == 200:
        geo_data = response.json()
        logger.debug(f"geolocation data fetched")
        return geo_data
    else:
        logger.error(f"Error fetching data: {response.status_code}")
        return {}



#TODO: retirer ca quand on aura fini
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
        mode = input("quel mode (current ou forecast): ")
        fetchWeatherData(city, country, mode)
        

    # old data cleaner setup
    """
    cleaning_thread = threading.Thread(target=houseKeeper)
    cleaning_thread.daemon = True  # This will make the thread close when the main program ends
    cleaning_thread.start()
    """

    # Main thread setup
    main_thread = threading.Thread(target=main_task)
    main_thread.start()
    main_thread.join()  # Wait for the main thread to finish

if __name__ == "__main__":
    main()
