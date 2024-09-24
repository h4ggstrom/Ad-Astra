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
def requestBuilder(city, country, apiKey):
    url = "http://api.openweathermap.org/data/2.5/weather?q="
    url += city + "," + country
    url += "&appid=" + dotenv_values["DISCORD_TOKEN"]
    return url