import discord
import requests
import os

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

intents = discord.Intents.default()
intents.voice_states = True

client = discord.Client(intents=intents)

@client.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        message = f"🔊 Chat vocale attiva su Discord!\nCanale: {after.channel.name}"
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        })

client.run(DISCORD_TOKEN)
