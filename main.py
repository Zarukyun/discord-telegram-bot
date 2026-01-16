import discord
import requests
import os

DISCORD_TOKEN = os.getenv("MTQzNTM5MTYwOTk2NDU5NzM1Mg.GMMNVc.g9FFtezxr12dij_Hh981gu3xM_ZSWl9QJmOW_I")
TELEGRAM_TOKEN = os.getenv("8463652179:AAFGAV3sj70fjpIc7nqtd_0SD6ZzsyH6Z_o")
TELEGRAM_CHAT_ID = os.getenv("1002369421733")

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
