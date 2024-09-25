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

import config as cfg

def requestBuilder(input_url: str, city: str, country: str) -> str:
    """this function is used to build the url for the request to the OpenWeatherMap API

    Args:
        input_url (str): the base URL for the API request
        city (str): the city for which we want the weather
        country (str): the country of the city

    Returns:
        str: the url for the request 
    """

    # building the url
    url = input_url
    url += city + "," + country
    url += "&APPID=" + cfg.WEATHER_TOKEN
    return url

# use example, TODO: remove this
print("EXEMPLE POUR LA METEO ACTUELLE A PARIS : \n")
print(requestBuilder(cfg.CURRENT_WEATHER_URL, "Paris", "fr"))
print("\n ############################## \n \n EXEMPLE POUR LES PREVISIONS HEURE PAR HEURE A PARIS :")
print(requestBuilder(cfg.HOURLY_FORECAST_URL, "Paris", "fr"))