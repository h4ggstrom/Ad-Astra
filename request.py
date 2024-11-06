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
import aaLogger as aaL

# Initialize the aaL.logger
aaL.logger.add("utils/Ad-Astra.log", rotation="500 MB", level="DEBUG")

def fetchWeatherData(lat: float, lon: float, mode: str) -> None:
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
    output_file: str
    
    if (mode == "current"):
        base_url = cfg.CURRENT_WEATHER_URL
    elif (mode == "forecast"):
        base_url = cfg.HOURLY_FORECAST_URL
    else:
        aaL.logger.error("Invalid mode. Please use 'current' or 'forecast'.")
        return
    
    # Check if the data already exists (aka if there is a request that was called less than an hour ago)
    if os.path.exists(f"data/{lat}_{lon}_{mode}.json"):
        aaL.logger.warning(f"Data for {lat}; {lon} already exists. Skipping request.")
        return
        
    # Make the API request
    request_url = base_url + f"lat={lat}&lon={lon}&appid=" + cfg.WEATHER_TOKEN + "&cnt=12"
    response = requests.get(request_url)
    
    """
    If data is fetched correctly, we save it in a file with the following format: date_hour_lat_lon_Mode.json
    if not, we raise an error
    """
    if response.status_code == 200:
        weather_data = response.json()
        # Ensure the 'data' directory exists
        os.makedirs('data', exist_ok=True)

        # Get the current date and time for the file's name
        now = datetime.now()

        # Define the path for the output file with the new format
        output_file = os.path.join('data', f"{lat}_{lon}_{mode}.json")
        aaL.logger.info(f"{mode} for {lat}; {lon} request data saved in {output_file}")
        
        # Write the weather data to the file
        with open(output_file, 'w') as file:
            json.dump(weather_data, file, indent=4)
        
    else:
        aaL.logger.error(f"Error fetching data: {response.status_code}")

    
def houseKeeper() -> None:
    """this function deletes files older than one hour in the data folder.
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
        aaL.logger.error("This function should be run in a separate thread to avoid blocking the main program.")
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
                    aaL.logger.info(f"Deleted old file: {file_path}")
        time.sleep(60)
        

def forecastFetch(json_file: str) -> list:
    """this function is used to extract the relevant informations from the json file containing the forecast data

    Args:
        json_file (str): the json file path

    Returns:
        list: the list containing the relevant informations
    """
    
    #internal variables
    data: dict
    dt: int
    humidity: int
    temp: float
    weather: str
    cloudiness: int
    wind_speed: float
    pop: float
    weather_info: dict
    info_list: list
    
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        aaL.logger.error(f"File not found: {json_file}")
        return []
    except json.JSONDecodeError:
        aaL.logger.error(f"Error decoding JSON from file: {json_file}")
        return []
        
    info_list = []
    
    for i in data['list']:
        dt = datetime.fromtimestamp(i['dt']).strftime('%H')
        humidity = i['main']['humidity']
        temp = i['main']['temp']
        weather = i['weather'][0]['description']
        cloudiness = i['clouds']['all']
        wind_speed = i['wind']['speed']
        pop = i['pop']

        weather_info = {
            'dt': dt,
            'humidity': humidity,
            'temp': temp,
            'weather': weather,
            'cloudiness': cloudiness,
            'wind_speed': wind_speed,
            'pop': pop
        }
        
        info_list.append(weather_info)
        
    return info_list


def getCoordinates(zip: int, country: str) -> dict:
    """returns coordinates of a specific location from a zip code and a country

    Args:
        zip (int): zip code of the location
        country (str): country of the location

    Returns:
        dict: the dictionary containing the coordinates
    """
    #internal variables
    rq_url: str
    coordinates: dict
    
    rq_url = cfg.GEOLOC_URL
    rq_url += f"zip?zip={zip},{country}"
    rq_url += "&appid=" + cfg.WEATHER_TOKEN
    coordinates = (requests.get(rq_url)).json()
    
    if coordinates == None:
        aaL.logger.error("fetch failed")
    else:
        aaL.logger.info("coordinates fetched")
    
    return coordinates
    
def main():
    coords = getCoordinates(75000, "FR")
    wd = fetchWeatherData(coords['lat'], coords['lon'], "forecast")
    forecasted_data = forecastFetch("data/48.8534_2.3488_forecast.json")
    print(forecasted_data)
    
if __name__ == "__main__":
    main()