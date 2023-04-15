import discord
from miio.airpurifier import AirPurifier
from miio.exceptions import DeviceException

client = discord.Client()
device_ip = "192.168.1.100"  # replace with your air purifier's IP address
device_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # replace with your air purifier's token
air_purifier = AirPurifier(device_ip, device_token)

async def turn_on():
    try:
        await air_purifier.on()
        return "Air purifier turned on."
    except DeviceException:
        return "Unable to turn on air purifier."

async def turn_off():
    try:
        await air_purifier.off()
        return "Air purifier turned off."
    except DeviceException:
        return "Unable to turn off air purifier."

async def get_temperature():
    try:
        temperature = await air_purifier.temperature()
        return f"Current temperature: {temperature}°C"
    except DeviceException:
        return "Unable to retrieve temperature."

async def get_humidity():
    try:
        humidity = await air_purifier.humidity()
        return f"Current humidity: {humidity}%"
    except DeviceException:
        return "Unable to retrieve humidity."

async def get_aqi():
    try:
        aqi = await air_purifier.aqi()
        return f"Current AQI: {aqi}"
    except DeviceException:
        return "Unable to retrieve AQI."

async def set_fan_level(level):
    try:
        await air_purifier.set_favorite_level(level)
        return f"Fan speed set to level {level}."
    except DeviceException:
        return f"Unable to set fan speed to level {level}."

@client.event
async def on_ready():
    print("Bot is ready.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "!on":
        response = await turn_on()
        await message.channel.send(response)

    elif message.content == "!off":
        response = await turn_off()
        await message.channel.send(response)

    elif message.content == "!temperature":
        response = await get_temperature()
        await message.channel.send(response)

    elif message.content == "!humidity":
        response = await get_humidity()
        await message.channel.send(response)

    elif message.content == "!aqi":
        response = await get_aqi()
        await message.channel.send(response)

    elif message.content.startswith("!fan "):
        try:
            level = int(message.content.split(" ")[1])
            if level in range(1, 4):
                response = await set_fan_level(level)
            else:
                response = "Fan speed level must be between 1 and 3."
        except ValueError:
            response = "Invalid fan speed level."
        await message.channel.send(response)

client.run("YOUR_DISCORD_BOT_TOKEN")
