import discord
import requests
import os
import sys

# Recupera le variabili d'ambiente
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Controlla che tutte le variabili siano presenti
missing_vars = []
if DISCORD_TOKEN is None:
    missing_vars.append("DISCORD_TOKEN")
if TELEGRAM_TOKEN is None:
    missing_vars.append("TELEGRAM_TOKEN")
if TELEGRAM_CHAT_ID is None:
    missing_vars.append("TELEGRAM_CHAT_ID")

if missing_vars:
    print(f"Errore: le seguenti variabili d'ambiente non sono impostate: {', '.join(missing_vars)}")
    sys.exit(1)  # Ferma il bot se mancano variabili

# Configura gli intents di Discord
intents = discord.Intents.default()
intents.voice_states = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot avviato come {client.user}")

@client.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        message = f"🔊 Chat vocale attiva su Discord!\nCanale: {after.channel.name} - UNISCITI ANCHE TU https://discord.gg/wYfvyWEK6c @LordMacbeth @Ardentsideburns @I_M_81 Aleksis Flavia @tedoli @RobertoMaurizzi @LkMsWb @Luinmir @Kyarushiro @Fumettoillogic https://gifdb.com/images/high/sailor-moon-sailor-scouts-3tih4dlavgr6x5pa.gif"
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        try:
            response = requests.post(url, data={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message
            })
            if not response.ok:
                print(f"Errore invio Telegram: {response.text}")
        except Exception as e:
            print(f"Eccezione invio Telegram: {e}")

# Avvia il bot Discord
client.run(DISCORD_TOKEN)
