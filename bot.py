"""
TODO: supprimer ce commentaire une fois qu'on aura fini le fichier

Le fichier bot.py va se charger de gérer les interactions avec l'API Discord. (#copilot)

En gros, va pas y avoir grand chose à faire ici. Juste le bot va se connecter à Discord, et renvoyer les commandes vers le main.py, pour qu'il les traites
Je pense ca va partir sur un gros tuto ytb un de ces jours, et inchallah ca va bien se passer.

"""

import discord
import config as cfg

# the bot needs to read commands (but only commands, not all messages), and tag users, if needed
intents = discord.Intents.default()
intents.message_content = False
intents.messages = True
intents.members = True

# creating the client
client = discord.Client(intents=intents) # intents on the left refers to the Client class variable, intents on the right refers to the parameter

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
   

# tbh this try/catch section is useless considering the token doesn't expire (and works), but let's call that *code quality* :upside_down:
try:
    client.run(cfg.DISCORD_TOKEN)
except discord.errors.LoginFailure:
    print("Invalid token")