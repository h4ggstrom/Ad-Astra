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
from loguru import logger


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
    locations: dict
    
    newLoc = {
        "ville": ville,
        "pays": pays,
        "latitude": latitude,
        "longitude": longitude
    }
    
    locFile = './utils/locations.json'
    print(locFile)
    if os.path.exists(locFile):
        logger.info(f"opening {locFile}")
        with open(locFile, 'r', encoding='utf-8') as f:
            locations = json.load(f)
    else:
        logger.info(f"creating {locFile}")
        locations = {}
    
    if nom not in locations:
        locations[nom] = []
    
    locations[nom].append(newLoc)
    
    with open(locFile, 'w', encoding='utf-8') as f:
        json.dump(locations, f, ensure_ascii=False, indent=4)
        
def main():
    # Test the addnewLoc function
    addnewLoc("Eiffel Tower", "Paris", "France", 48.8584, 2.2945)
    addnewLoc("Statue of Liberty", "New York", "USA", 40.6892, -74.0445)
    addnewLoc("Colosseum", "Rome", "Italy", 41.8902, 12.4922)

if __name__ == "__main__":
    main()