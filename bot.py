"""
TODO: supprimer ce commentaire une fois qu'on aura fini le fichier

Le fichier client.py va se charger de gérer les interactions avec l'API Discord. (#copilot)

En gros, va pas y avoir grand chose à faire ici. Juste le client va se connecter à Discord, et renvoyer les commandes vers le main.py, pour qu'il les traites
Je pense ca va partir sur un gros tuto ytb un de ces jours, et inchallah ca va bien se passer.

"""
import discord
import config as cfg
from discord import app_commands
import commandsManager as cm


# declaring variables
intents: discord.Intents
client: discord.Client


# the client needs to read commands (but only commands, not all messages), and tag users, if needed
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.members = True

# creating the client
client = discord.Client(intents=intents)  # intents on the left refers to the client class variable, intents on the right refers to the parameter
tree = app_commands.CommandTree(client)
guild_id = discord.Object(id="1168264156500217966") 


@client.event
async def on_ready():
    await tree.sync(guild=guild_id)
    print(f'Logged in as {client.user}')


@tree.command(name="zioum", description="random bullshit go", guild=guild_id)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("https://tenor.com/view/bing-gif-25601964")


# TODO: add a command to add a location to the list
@tree.command(name="add_location", description="add a location to the list", guild=guild_id)
async def add_location(interaction: discord.Interaction, nom: str, ville: str, pays: str, latitude: float, longitude: float):
    cm.addnewLoc(nom, ville, pays, latitude, longitude)
    await interaction.response.send_message("location added :thumbsup:")


# TODO: add a command to delete a location from the list
@tree.command(name="delete_location", description="delete a location from the list", guild=guild_id)
async def delete_location(interaction: discord.Interaction):
    await interaction.response.send_message("https://tenor.com/view/you-have-been-removed-from-the-list-gif-20918111")


# TODO: add a command to list all the locations
@tree.command(name="list_locations", description="list all the locations", guild=guild_id)
async def list_locations(interaction: discord.Interaction):
    await interaction.response.send_message("https://tenor.com/view/you-have-been-removed-from-the-list-gif-20918111")
    

# TODO: add a command to edit an existing location
@tree.command(name="edit_location", description="edit an existing location", guild=guild_id)
async def edit_location(interaction: discord.Interaction):
    await interaction.response.send_message("https://tenor.com/view/you-have-been-removed-from-the-list-gif-20918111")


@tree.command(name="get_current_weather", description="send a report of the current weather at specified location", guild=guild_id)
async def current_weather(interaction: discord.Interaction):
    await interaction.response.send_message("https://tenor.com/view/you-have-been-removed-from-the-list-gif-20918111")




# tbh this try/catch section is useless considering the token doesn't expire (and works), but let's call that *code quality* :upside_down:
def run():
    try:
        client.run(cfg.DISCORD_TOKEN)   
    except discord.errors.LoginFailure:
        print("Invalid token")
        
if __name__ == "__main__":
    run() 