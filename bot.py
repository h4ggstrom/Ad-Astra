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
import aaLogger as aaL
import request as rq


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
async def ping(interaction: discord.Interaction) -> None:
    """test command to check if the bot is working. Simply sends a GIF in a discord channel.

    Args:
        interaction (discord.Interaction): discord interaction object
    """
    await interaction.response.send_message("https://tenor.com/view/bing-gif-25601964")


@tree.command(name="add_location", description="add a location to the list", guild=guild_id)
async def add_location(interaction: discord.Interaction, name: str, city: str, country: str, latitude: float, longitude: float) -> None:
    """slash command to add a location to the list

    Args:
        interaction (discord.Interaction): the interaction object
        name (str): name of the location
        city (str): closest city to the location
        country (str): country of the location
        latitude (float): latitude of the location
        longitude (float): longitude of the location
    """
    
    cm.addnewLoc(name, city, country, latitude, longitude)
    await interaction.response.send_message("location added :thumbsup:")


@tree.command(name="delete_location", description="delete a location from the list", guild=guild_id)
async def delete_location(interaction: discord.Interaction, name: str) -> None:
    """slash command to delete a location from the list

    Args:
        interaction (discord.Interaction): the interaction object
        name (str): the name of the location to delete
    """
    #internal variable
    code: int
    
    code = cm.removeLocation(name)
    
    # error handling
    if code == 0:
        await interaction.response.send_message("location deleted :thumbsup:")
    elif code == 1:
        await interaction.response.send_message("location not found :thumbsdown:")
    elif code == 2:
        await interaction.response.send_message("error location file not found :sob:")
    else:
        await interaction.response.send_message(f"error code: {code}")


@tree.command(name="list_locations", description="list all the locations", guild=guild_id)
async def list_locations(interaction: discord.Interaction) -> None:
    """slash command to list all the locations

    Args:
        interaction (discord.Interaction): discord interaction object
    """
    #internal variables
    string: str
    
    string = ""
    for i in cm.getFormattedLocations():
        string += f"{i}\n"
    await interaction.response.send_message(f"```{string}```")

@tree.command(name="get_location", description="get the details of a location", guild=guild_id)
async def get_location(interaction: discord.Interaction, name: str) -> None:
    """display the details of a location

    Args:
        interaction (discord.Interaction): discord interaction object
        name (str): name of the location
    """
    # internal variables
    loc: dict
    loc_str: str
    
    loc = cm.getLocation(name)
    if loc == None:
        await interaction.response.send_message("location not found :thumbsdown:")
    else:
        loc_str = ""
        for k, v in loc.items():
            loc_str += f"{k}: {v}\n"
        await interaction.response.send_message(f"```json\n{loc_str}\n```")


@tree.command(name="get_current_weather", description="send a report of the current weather at specified location", guild=guild_id)
async def current_weather(interaction: discord.Interaction) -> None:
    await interaction.response.send_message("https://tenor.com/view/you-have-been-removed-from-the-list-gif-20918111")


@tree.command(name="coordinates", description="get the coordinates of a location", guild=guild_id)
async def coordinates(interaction: discord.Interaction, zip: int, country: str) -> None:
    coordinates = rq.getCoordinates(zip, country)
    if coordinates == None:
        await interaction.response.send_message("fetch failed :upside_down:")
    coord = "values \n"
    for k, v in coordinates.items():
        coord += f"{k}: {v}\n"
    await interaction.response.send_message(f"```json\n {coord}\n```")
    


# tbh this try/catch section is useless considering the token doesn't expire (and works), but let's call that *code quality* :upside_down:
def run():
    try:
        client.run(cfg.DISCORD_TOKEN)   
    except discord.errors.LoginFailure:
        aaL.logger.error("Invalid token.")
        
if __name__ == "__main__":
    run() 