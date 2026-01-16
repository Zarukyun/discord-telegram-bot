import discord
import requests
import os
import sys
import json
import time # Necessario per gestire il timeout

# Recupera le variabili d'ambiente
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Controlla che tutte le variabili siano presenti
missing_vars = []
if DISCORD_TOKEN is None: missing_vars.append("DISCORD_TOKEN")
if TELEGRAM_TOKEN is None: missing_vars.append("TELEGRAM_TOKEN")
if TELEGRAM_CHAT_ID is None: missing_vars.append("TELEGRAM_CHAT_ID")

if missing_vars:
    print(f"Errore: le seguenti variabili d'ambiente non sono impostate: {', '.join(missing_vars)}")
    sys.exit(1)

# Configurazione Cooldown (5 minuti = 300 secondi)
COOLDOWN_SECONDS = 300
last_message_time = 0 

# Configura gli intents di Discord
intents = discord.Intents.default()
intents.voice_states = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot avviato come {client.user}")

@client.event
async def on_voice_state_update(member, before, after):
    global last_message_time
    
    # Rileva quando qualcuno entra in un canale vocale (e prima non c'era)
    if before.channel is None and after.channel is not None:
        
        current_time = time.time()
        
        # Controlla se sono passati almeno 300 secondi dall'ultimo messaggio
        if current_time - last_message_time < COOLDOWN_SECONDS:
            print("Evento ignorato: cooldown attivo.")
            return

        # 1. Configurazione Messaggio e Media
        discord_link = "https://discord.gg/wYfvyWEK6c"
        gif_url = "https://gifdb.com/images/high/sailor-moon-sailor-scouts-3tih4dlavgr6x5pa.gif"
        # Rimossi Aleksis e Flavia come richiesto
        usernames = "@LordMacbeth @Ardentsideburns @I_M_81 @tedoli @RobertoMaurizzi @LkMsWb @Luinmir @Kyarushiro @Fumettoillogic"
        
        caption = (
            f"🚨 <b>VOCALE ATTIVA SU DISCORD</b> 🚨\n\n"
            f"Canale: <b>{after.channel.name.upper()}</b>\n\n"
            f"📢 {usernames}"
        )

        # 2. Creazione del Bottone Inline
        reply_markup = {
            "inline_keyboard": [[
                {"text": "🚀 UNISCITI ORA", "url": discord_link}
            ]]
        }

        # 3. Invio tramite sendAnimation
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendAnimation"
        
        try:
            response = requests.post(url, data={
                "chat_id": TELEGRAM_CHAT_ID,
                "animation": gif_url,
                "caption": caption,
                "parse_mode": "HTML",
                "reply_markup": json.dumps(reply_markup)
            })
            
            if response.ok:
                # Aggiorna l'orario dell'ultimo invio riuscito
                last_message_time = current_time
                print("Messaggio Telegram inviato correttamente.")
            else:
                print(f"Errore invio Telegram: {response.text}")
                
        except Exception as e:
            print(f"Eccezione invio Telegram: {e}")

# Avvia il bot Discord
client.run(DISCORD_TOKEN)
