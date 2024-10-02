import os
import json

""" 
En gros, ce fichier va contenir tous les outils nécessaires pour gérer les localisations.
C'est  à dire :
    - les ajouter
    - les supprimer
    - les modifier
    - les lister
"""

def ajouter_localisation(nom, ville, pays, latitude, longitude):
    localisation = {
        "nom": nom,
        "ville": ville,
        "pays": pays,
        "latitude": latitude,
        "longitude": longitude
    }
    
    fichier_localisations = os.path.join(os.path.dirname(__file__), 'localisations.json')
    
    if os.path.exists(fichier_localisations):
        with open(fichier_localisations, 'r', encoding='utf-8') as f:
            localisations = json.load(f)
    else:
        localisations = []
    
    localisations.append(localisation)
    
    with open(fichier_localisations, 'w', encoding='utf-8') as f:
        json.dump(localisations, f, ensure_ascii=False, indent=4)