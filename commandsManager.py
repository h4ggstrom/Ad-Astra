""" 
TODO: supp le comm quand on aura fini le fichier

Ce fichier va gérer les inputs de commandes, notamment pour les locations et les store dans un fichier,
histoire que le bot puisse les utiliser automatiquement plus tard.

TODO: editLocation

Pour plus tard, si on a la foi:
TODO: setThreshold
"""

import os
import json
from loguru import logger


def addnewLoc(name: str, city: str, country: str, latitude: float, longitude: float) -> None:
    """add a locatisation to the list in the file. If it doesn't exist, create it.

    Args:
        name (str): name of the location (defined by the user)
        city (str): closest city to the location
        country (str): country of the location
        latitude (float): latitude of the location
        longitude (float): longitude of the location
    """
    #internal variables
    newLoc: dict
    locFile: str
    locations: dict
    
    newLoc = {
        "city": city,
        "country": country,
        "latitude": latitude,
        "longitude": longitude
    }
    
    locFile = './utils/locations.json'
    
    if os.path.exists(locFile):
        logger.info(f"opening {locFile}")
        with open(locFile, 'r', encoding='utf-8') as f:
            locations = json.load(f)
    else:
        logger.info(f"creating {locFile}")
        locations = {}
    
    if name not in locations:
        locations[name] = []
    
    locations[name].append(newLoc)
    
    with open(locFile, 'w', encoding='utf-8') as f:
        json.dump(locations, f, ensure_ascii=False, indent=4)

def removeLocation(name: str) -> int:
    """Remove a location from the list in the file.

    Args:
        name (str): name of the location to remove
        
    Returns:
        int: 2 if the file doesn't exist, 1 if the location is not found, 0 if the location is successfully removed
    """
    #internal variables
    locFile: str
    locations: dict
    
    locFile = './utils/locations.json'
    if not os.path.exists(locFile):
        logger.error(f"{locFile} does not exist.")
        return 2
    
    with open(locFile, 'r', encoding='utf-8') as f:
        locations = json.load(f)
    
    if name in locations:
        del locations[name]
        logger.info(f"Removed location: {name}")
    else:
        logger.warning(f"Location {name} not found.")
        return 1
    
    with open(locFile, 'w', encoding='utf-8') as f:
        json.dump(locations, f, ensure_ascii=False, indent=4)
    
    return 0

def getFormattedLocations() -> list:
    """Get formatted locations from the locations file.

    Returns:
        list: A list of formatted location strings in the format "{name} ==> {latitude}, {longitude}"
    """
    #internal variables
    locFile: str
    locations: dict
    formatted_locations: list
    
    
    locFile = './utils/locations.json'
    if not os.path.exists(locFile):
        logger.error(f"{locFile} does not exist.")
        return None
    
    with open(locFile, 'r', encoding='utf-8') as f:
        locations = json.load(f)
    
    formatted_locations = []
    for name, locs in locations.items():
        for loc in locs:
            formatted_locations.append(f"{name} ==> {loc['latitude']}; {loc['longitude']}")
    
    return formatted_locations
        
def getLocation(name: str) -> dict:
    """Get the location details of a location.

    Args:
        name (str): name of the location to get

    Returns:
        dict: A dictionary containing the location details
    """
    #internal variables
    locFile: str
    locations: dict
    
    locFile = './utils/locations.json'
    if not os.path.exists(locFile):
        logger.error(f"{locFile} does not exist.")
        return None
    
    with open(locFile, 'r', encoding='utf-8') as f:
        locations = json.load(f)
    
    if name in locations:
        return locations[name][0]
    else:
        logger.warning(f"Location {name} not found.")
        return None

def main():
    # Test the addnewLoc function
    addnewLoc("Eiffel Tower", "Paris", "France", 48.8584, 2.2945)
    addnewLoc("Statue of Liberty", "New York", "USA", 40.6892, -74.0445)
    addnewLoc("Colosseum", "Rome", "Italy", 41.8902, 12.4922)

if __name__ == "__main__":
    main()