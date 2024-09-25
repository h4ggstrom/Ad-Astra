import os
from dotenv import load_dotenv

""" 
TODO: supp le comm quand on aura fini le fichier

Ce fichier va centraliser les tokens, et les variables du dotenv, pour éviter d'avoir à load la librairie à chaque fois qu'on en a besoin.
Donc pas un gros fichier, mais un fichier utile.
"""
load_dotenv()

# Centralize variables from .env
TOKEN = os.getenv('TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')