"""
TODO: supprimer ce commentaire une fois qu'on aura fini le fichier

Le fichier bot.py va se charger de gérer les interactions avec l'API Discord. (#copilot)

En gros, va pas y avoir grand chose à faire ici. Juste le bot va se connecter à Discord, et renvoyer les commandes vers le main.py, pour qu'il les traites
Je pense ca va partir sur un gros tuto ytb un de ces jours, et inchallah ca va bien se passer.

"""

import discord
import config as cfg

# Define the intents
intents = discord.Intents.default()
intents.messages = True
intents.members = True

# creating the client
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    
try:
    client.run(cfg.DISCORD_TOKEN)
except discord.errors.LoginFailure:
    print("Invalid token")