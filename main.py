import os
from dotenv import load_dotenv
import discord
from discord import app_commands
import requests

load_dotenv()

API_KEY = os.getenv("OPENWEATHERAPI_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

class WeatherBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        await self.tree.sync()
        print(f"✅ Logged in as {self.user}")

print("OpenWeather key loaded:", bool(API_KEY))
print("Discord token loaded:", bool(DISCORD_TOKEN))

client = WeatherBot()

@client.tree.command(name="weather", description="Get current weather for a city 🌤️")
@app_commands.describe(city="Enter the city name")
async def weather(interaction: discord.Interaction, city: str):
    await interaction.response.defer(thinking=True)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=en"
    response = requests.get(url).json()
    print("Request URL:", url)
    print("API Response:", response)

    if response.get("cod") != 200:
        await interaction.followup.send(f"❌ City **{city}** not found.")
        return

    name = response["name"]
    country = response["sys"]["country"]
    temp = response["main"]["temp"]
    desc = response["weather"][0]["description"]
    humidity = response["main"]["humidity"]
    icon = response["weather"][0]["icon"]

    embed = discord.Embed(
        title=f"🌤️ Weather in {name}, {country}",
        description=f"**{desc.capitalize()}**",
        color=discord.Color.blue()
    )
    embed.add_field(name="🌡 Temperature", value=f"{temp} °C", inline=True)
    embed.add_field(name="💧 Humidity", value=f"{humidity}%", inline=True)
    embed.set_thumbnail(url=f"http://openweathermap.org/img/wn/{icon}@2x.png")

    await interaction.followup.send(embed=embed)

client.run(DISCORD_TOKEN)
