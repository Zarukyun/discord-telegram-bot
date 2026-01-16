import discord
import requests
import os
import sys
import json
import random

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

# Pool di GIF personalizzato
GIF_POOL = [
    "https://gifdb.com/images/high/sailor-moon-sailor-scouts-3tih4dlavgr6x5pa.gif",
    "https://i.makeagif.com/media/12-14-2022/ka2PIJ.gif",
    "https://i.pinimg.com/originals/a3/83/1e/a3831e928fdac37166b823b8a7b8efab.gif",
    "https://media.tenor.com/c0WNBHq-K58AAAAM/anime-memes.gif",
    "https://i.makeagif.com/media/9-08-2015/cCez20.gif",
    "https://latanadiachernar.wordpress.com/wp-content/uploads/2018/03/oscar6.gif",
    "https://i.makeagif.com/media/3-21-2020/EpemtZ.gif",
    "https://media.tenor.com/qy0292ijpOkAAAAM/tiger-mask-tiger-man.gif",
    "https://animesher.com/orig/1/197/1977/19770/animesher.com_revolutionary-girl-utena-pretty-gif-1977086.gif"
]

# Configura gli intents di Discord
intents = discord.Intents.default()
intents.voice_states = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot avviato come {client.user}")

@client.event
async def on_voice_state_update(member, before, after):
    # Rileva quando qualcuno entra in un canale vocale (e prima non era in nessun canale)
    if before.channel is None and after.channel is not None:
        
        # 1. Configurazione Messaggio e Media
        discord_link = "https://discord.gg/wYfvyWEK6c"
        selected_gif_url = random.choice(GIF_POOL)
        
        # Nickname Telegram aggiornati
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

        # 3. Invio tramite sendAnimation (gestisce le GIF come video animati)
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendAnimation"
        
        try:
            response = requests.post(url, data={
                "chat_id": TELEGRAM_CHAT_ID,
                "animation": selected_gif_url,
                "caption": caption,
                "parse_mode": "HTML",
                "reply_markup": json.dumps(reply_markup)
            })
            
            if response.ok:
                print(f"Messaggio inviato con GIF: {selected_gif_url}")
            else:
                print(f"Errore invio Telegram: {response.text}")
                
        except Exception as e:
            print(f"Eccezione invio Telegram: {e}")

# Avvia il bot Discord
client.run(DISCORD_TOKEN)
