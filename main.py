import discord
from discord.ext import tasks # Necessario per il ciclo ogni 30 min
import requests
import os
import sys
import json
import random

# --- CONFIGURAZIONE ---
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
DISCORD_LINK = "https://discord.gg/wYfvyWEK6c"
USERNAMES = "@LordMacbeth @Ardentsideburns @I_M_81 @tedoli @RobertoMaurizzi @LkMsWb @Luinmir @Kyarushiro @Fumettoillogic"

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

if not all([DISCORD_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID]):
    print("Errore: Variabili d'ambiente mancanti.")
    sys.exit(1)

intents = discord.Intents.default()
intents.voice_states = True
client = discord.Client(intents=intents)

# Variabile per tracciare lo stato della chiamata
current_voice_channel = None

def send_telegram_media(caption, gif_url=None):
    """Funzione di supporto per inviare messaggi su Telegram"""
    method = "sendAnimation" if gif_url else "sendMessage"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/{method}"
    
    reply_markup = {"inline_keyboard": [[{"text": "🚀 UNISCITI ORA", "url": DISCORD_LINK}]]}
    
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "parse_mode": "HTML",
        "reply_markup": json.dumps(reply_markup)
    }
    
    if gif_url:
        payload["animation"] = gif_url
        payload["caption"] = caption
    else:
        payload["text"] = caption

    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Errore Telegram: {e}")

# --- LOOP OGNI 30 MINUTI ---
@tasks.loop(minutes=30)
async def check_still_in_call():
    global current_voice_channel
    if current_voice_channel:
        # Controlla se c'è ancora qualcuno nel canale
        if len(current_voice_channel.members) > 0:
            msg = f"⏳ <b>SIAMO ANCORA IN CHIAMATA!</b>\nCanale: <b>{current_voice_channel.name.upper()}</b>\n\nNon farti pregare, entra! {USERNAMES}"
            send_telegram_media(msg, random.choice(GIF_POOL))
        else:
            current_voice_channel = None # Reset se il canale è vuoto

@client.event
async def on_ready():
    print(f"Bot avviato come {client.user}")
    check_still_in_call.start() # Avvia il ciclo temporizzato

@client.event
async def on_voice_state_update(member, before, after):
    global current_voice_channel

    # INIZIO CHIAMATA: Qualcuno entra e prima non c'era nessuno in nessun canale
    if before.channel is None and after.channel is not None:
        # Se è il primo ad entrare in assoluto (o dopo che il canale era vuoto)
        if len(after.channel.members) == 1:
            current_voice_channel = after.channel
            msg = f"🚨 <b>VOCALE ATTIVA SU DISCORD</b> 🚨\nCanale: <b>{after.channel.name.upper()}</b>\n\n📢 {USERNAMES}"
            send_telegram_media(msg, random.choice(GIF_POOL))

    # FINE CHIAMATA: Qualcuno esce
    if before.channel is not None and after.channel is None:
        # Se il canale che è stato appena lasciato è ora vuoto
        if len(before.channel.members) == 0:
            current_voice_channel = None
            msg = "😴 <b>LA CHAT VOCALE È FINITA</b>\nPer oggi è tutto, ci si vede alla prossima! 👋"
            # Per la fine chiamata inviamo solo testo, senza GIF (opzionale)
            send_telegram_media(msg)

client.run(DISCORD_TOKEN)
