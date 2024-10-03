""" 
TODO: supp le comm quand on aura fini le fichier

Ce fichier va gérer les inputs de commandes, notamment pour les locations et les store dans un fichier,
histoire que le bot puisse les utiliser automatiquement plus tard.

TODO: addLocation
TODO: editLocation
TODO: removeLocation

Pour plus tard, si on a la foi:
TODO: setThreshold
"""

import os
import json


def addnewLoc(nom: str, ville: str, pays: str, latitude: float, longitude: float) -> None:
    """add a locatisation to the list in the file. If it doesn't exist, create it.

    Args:
        nom (str): name of the location (defined by the user)
        ville (str): closest city to the location
        pays (str): country of the location
        latitude (float): latitude of the location
        longitude (float): longitude of the location
    """
    
    #internal variables
    newLoc: dict
    locFile: str
    locations: list
    
    
    newLoc = {
        "nom": nom,
        "ville": ville,
        "pays": pays,
        "latitude": latitude,
        "longitude": longitude
    }
    
    locFile = os.path.join(os.path.dirname(__file__), 'locations.json')
    
    if os.path.exists(locFile):
        with open(locFile, 'r', encoding='utf-8') as f:
            locations = json.load(f)
    else:
        locations = []
    
    locations.append(newLoc)
    
    with open(locFile, 'w', encoding='utf-8') as f:
        json.dump(locations, f, ensure_ascii=False, indent=4)