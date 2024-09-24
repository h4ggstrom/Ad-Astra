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
from dotenv import load_dotenv
import os

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

def requestBuilder(city, country,):
    # Vérifier si les variables d'environnement sont chargées correctement
    weather_token = os.getenv("WEATHER_TOKEN")
    if weather_token is None:
        print("Erreur : weather_token n'est pas défini dans le fichier .env")
        return None
    
    weather_url = os.getenv("WEATHER_URL")
    if weather_url is None:
        print("Erreur : weather_url n'est pas défini dans le fichier .env")
        return None

    url = weather_url
    url += city + "," + country
    url += "&APPID=" + weather_token
    return url

# Exemple d'utilisation
print(requestBuilder("Paris", "fr"))