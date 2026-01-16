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
    sys.exit(1)

# Configura gli intents di Discord
intents = discord.Intents.default()
intents.voice_states = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot avviato come {client.user}")

@client.event
async def on_voice_state_update(member, before, after):
    # Rileva quando qualcuno entra in un canale vocale (e prima non c'era nessuno o lui non era in VC)
    if before.channel is None and after.channel is not None:
        
        # 1. Configurazione Messaggio
        discord_link = "https://discord.gg/wYfvyWEK6c"
        gif_url = "https://gifdb.com/images/high/sailor-moon-sailor-scouts-3tih4dlavgr6x5pa.gif"
        usernames = "@LordMacbeth @Ardentsideburns @I_M_81 @tedoli @RobertoMaurizzi @LkMsWb @Luinmir @Kyarushiro @Fumettoillogic Aleksis Flavia"
        
        caption = (
            f"🔊 <b>Chat vocale attiva su Discord!</b>\n"
            f"Canale: <b>{after.channel.name}</b>\n\n"
            f"<a href='{discord_link}'>👉 UNISCITI ANCHE TU</a>\n\n"
            f"{usernames}"
        )

        # 2. Utilizzo di sendAnimation per inviare la GIF come video
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendAnimation"
        
        try:
            response = requests.post(url, data={
                "chat_id": TELEGRAM_CHAT_ID,
                "animation": gif_url,
                "caption": caption,
                "parse_mode": "HTML"
            })
            
            if not response.ok:
                print(f"Errore invio Telegram: {response.text}")
        except Exception as e:
            print(f"Eccezione invio Telegram: {e}")

# Avvia il bot Discord
client.run(DISCORD_TOKEN)
