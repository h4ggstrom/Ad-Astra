"""
TODO: supprimer ce commentaire une fois qu'on aura fini le fichier

Le fichier client.py va se charger de gérer les interactions avec l'API Discord. (#copilot)

En gros, va pas y avoir grand chose à faire ici. Juste le client va se connecter à Discord, et renvoyer les commandes vers le main.py, pour qu'il les traites
Je pense ca va partir sur un gros tuto ytb un de ces jours, et inchallah ca va bien se passer.

"""
import json
import discord
import config as cfg
from discord import app_commands
import commandsManager as cm
import aaLogger as aaL
import request as rq
import os
from datetime import datetime
import threading


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
    aaL.logger.info(f"Logged in as {client.user.name} - {client.user.id}")


@tree.command(name="zioum", description="random bullshit go", guild=guild_id)
async def ping(interaction: discord.Interaction) -> None:
    """test command to check if the bot is working. Simply sends a GIF in a discord channel.

    Args:
        interaction (discord.Interaction): discord interaction object
    """
    await interaction.response.send_message("https://tenor.com/view/bing-gif-25601964")

# TODO: utiliser le code de la fonction coordinate pour simplifier les arguments
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
    
# TODO: ca, ca dégage une fois qu'on a fini d'implémenter l'affichage   
@tree.command(name="embed", description="Envoie un message embed", guild=guild_id)
async def embed(interaction: discord.Interaction) -> None:
    embed = discord.Embed(
        title="Prévisions Météo du Jour",
        description="Voici les prévisions météo complètes.",
        color=discord.Color.green(),
        url="https://example.com"
    )
    
    user = await client.fetch_user(interaction.user.id)
    embed.set_author(name=user.name, icon_url=user.avatar.url)
    embed.add_field(name="Ville", value="Paris", inline=False)
    embed.add_field(name="Température", value="18°C", inline=True)
    embed.add_field(name="Humidité", value="72%", inline=True)
    embed.set_thumbnail(url="https://openweathermap.org/img/wn/10d@2x.png")
    embed.set_image(url="https://example.com/weather-map.png")
    embed.set_footer(text="Dernière mise à jour : 12h00", icon_url="https://example.com/logo.png")
    embed.timestamp = discord.utils.utcnow()
    
    await interaction.response.send_message(embed=embed)
    
@tree.command(name="forecast", description="display a 12h hour forecast for a specific location", guild=guild_id)
async def forecast(interaction: discord.Interaction, name: str) -> None:
    loc = cm.getLocation(name)
    
    if loc is None:
        await interaction.response.send_message("location not found :thumbsdown:")
    else:
        rq.fetchWeatherData(loc['latitude'], loc['longitude'], "forecast")
        wd = rq.forecastFetch(f"data/{loc['latitude']}_{loc['longitude']}_forecast.json")
        if wd is None:
            await interaction.response.send_message("fetch failed :upside_down:")
        else:
            embed = discord.Embed(
                title=f"Prévisions Météo pour {name}- Heure par Heure",
                description="Voici les prévisions météo pour les 12 prochaines heures",
                color=discord.Color.purple()
            )
            
            for hour_data in wd:
                # Formatage de l'heure et des données
                badness = 0
                hour = hour_data['dt'] + ":00"
                weather = hour_data['weather'].capitalize()
                
                # cloudiness rating
                if hour_data['cloudiness'] < 20:
                    cloudiness = ":green_square: "
                elif 20 <= hour_data['cloudiness'] < 50:
                    cloudiness = ":orange_square: "
                    badness += 1
                else:
                    cloudiness = ":red_square: "
                    badness += 3
                cloudiness += f"Nuages: **{hour_data['cloudiness']}%**"
                
                
                # temperature rating
                if 0<(hour_data['temp'] - 273.15) and (hour_data['temp'] - 273.15)<10 :
                    temperature = ":green_square: "
                else:
                    temperature = ":orange_square: "
                    badness += 0.2
                temperature += f"Température: **{hour_data['temp'] - 273.15:.1f}°C**"  # Conversion de Kelvin en Celsius
                
                
                # humidity rating
                if hour_data['humidity'] < 50:
                    humidity = ":green_square: "
                elif 50 <= hour_data['humidity'] < 70:
                    humidity = ":orange_square: "
                    badness += 0.5
                else:
                    humidity = ":red_square: "
                    badness += 1
                humidity += f"Humidité: **{hour_data['humidity']}%**"
                
                
                # wind rating
                if hour_data['wind_speed'] < 2.78:
                    wind = ":green_square: "
                elif 2.78 <= hour_data['wind_speed'] < 6.94:
                    wind = ":orange_square: "
                    badness += 0.5
                else:
                    wind = ":red_square: "
                    badness += 1
                wind += f"Vent: **{hour_data['wind_speed']} m/s**"
                
                
                # pop rating
                if hour_data['pop'] < 0.02:
                    pop = ":green_square: "
                else:
                    pop = ":red_square: "
                    badness += 3
                pop += f"précipitations: **{hour_data['pop'] * 100}%**"
                
                # badness rating
                if badness < 2:
                    rating = "__***RATING: ***__:green_square:"
                elif badness < 3:
                    rating = "__***RATING: ***__:orange_square:"
                else:
                    rating = "__***RATING: ***__:red_square:"

                # Ajout de chaque champ pour chaque heure
                embed.add_field(name=hour, value=f"{rating}\n**{weather}**\n{cloudiness}\n{temperature}\n{humidity}\n{wind}\n{pop}", inline=True)
                # Get the last modified time of the JSON file

                file_path = f"data/{loc['latitude']}_{loc['longitude']}_forecast.json"
                last_modified_time = os.path.getmtime(file_path)
                last_modified_date = datetime.fromtimestamp(last_modified_time).strftime('%d/%m/%Y %H:%M:%S')

                # Add footer with the last modified date
                embed.set_footer(text=f"Dernière mise à jour : {last_modified_date}")
            await interaction.response.send_message(embed=embed)

# tbh this try/catch section is useless considering the token doesn't expire (and works), but let's call that *code quality* :upside_down:
def run():
    try:
        # Start the houseKeeper function in a separate daemon thread
        housekeeper_thread = threading.Thread(target=rq.houseKeeper, daemon=True)
        housekeeper_thread.start()
        if not housekeeper_thread.is_alive():
            aaL.logger.error("Housekeeper deamon failed to start.")
            return
        aaL.logger.debug("Housekeeper deamon started.")
        
        client.run(cfg.DISCORD_TOKEN)
    except discord.errors.LoginFailure:
        aaL.logger.error("Invalid token.")
        
if __name__ == "__main__":
    run() 