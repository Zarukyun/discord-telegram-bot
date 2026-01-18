import discord
from discord.ext import tasks
import requests
import os
import sys
import json
import random
import time
from datetime import datetime

# --- CONFIGURAZIONE ---
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
DISCORD_LINK = "https://discord.gg/wYfvyWEK6c"
USERNAMES_TAG = "@LordMacbeth @Ardentsideburns @I_M_81 @tedoli @RobertoMaurizzi @LkMsWb @Luinmir @Kyarushiro @Fumettoillogic"

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

# --- LOGICA DI STATO ---
current_voice_channel = None
start_time = None
last_start_msg_time = 0
COOLDOWN_START = 300  # 5 minuti in secondi

intents = discord.Intents.default()
intents.voice_states = True
client = discord.Client(intents=intents)

def send_telegram(caption, gif_url=None, show_button=True):
    method = "sendAnimation" if gif_url else "sendMessage"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/{method}"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "parse_mode": "HTML"}
    if show_button:
        payload["reply_markup"] = json.dumps({"inline_keyboard": [[{"text": "🚀 UNISCITI ORA", "url": DISCORD_LINK}]]})
    if gif_url:
        payload.update({"animation": gif_url, "caption": caption})
    else:
        payload["text"] = caption
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Errore Telegram: {e}")

# --- LOOP OGNI 90 MINUTI ---
@tasks.loop(minutes=90)
async def reminder_loop():
    global current_voice_channel
    if current_voice_channel and len(current_voice_channel.members) > 0:
        presenti = ", ".join([m.display_name for m in current_voice_channel.members])
        msg = (f"⏳ <b>SIAMO ANCORA IN CHIAMATA!</b>\n"
               f"Canale: <b>{current_voice_channel.name.upper()}</b>\n"
               f"Presenti ora: <b>{presenti}</b>\n\n"
               f"Unisciti a noi! {USERNAMES_TAG}")
        send_telegram(msg, random.choice(GIF_POOL))

@client.event
async def on_ready():
    print(f"Bot avviato come {client.user}")
    if not reminder_loop.is_running():
        reminder_loop.start()

@client.event
async def on_voice_state_update(member, before, after):
    global current_voice_channel, start_time, last_start_msg_time

    # INGRESSO IN VOCALE
    if before.channel is None and after.channel is not None:
        now = time.time()
        
        # Se è il primo in assoluto a entrare
        if len(after.channel.members) == 1:
            current_voice_channel = after.channel
            start_time = datetime.now()
            
            # Notifica inizio solo se fuori cooldown
            if now - last_start_msg_time > COOLDOWN_START:
                msg = (f"🚨 <b>VOCALE ATTIVA SU DISCORD</b> 🚨\n"
                       f"Canale: <b>{after.channel.name.upper()}</b>\n"
                       f"Iniziata da: <b>{member.display_name}</b>\n\n"
                       f"📢 {USERNAMES_TAG}")
                send_telegram(msg, random.choice(GIF_POOL))
                last_start_msg_time = now
        
        # Notifica per ogni persona che entra (sempre, senza tag)
        else:
            msg = f"👤 <b>{member.display_name}</b> è appena entrato in chiamata!"
            send_telegram(msg, show_button=True)

    # USCITA DALLA VOCALE
    elif before.channel is not None and after.channel is None:
        if len(before.channel.members) == 0:
            end_time = datetime.now()
            durata_str = "N/D"
            if start_time:
                durata = end_time - start_time
                ore, resto = divmod(int(durata.total_seconds()), 3600)
                minuti, _ = divmod(resto, 60)
                durata_str = f"{ore}h {minuti}m" if ore > 0 else f"{minuti} minuti"
            
            msg = (f"😴 <b>LA CHAT VOCALE È FINITA</b>\n"
                   f"Durata sessione: <b>{durata_str}</b>\n"
                   f"Ci si vede alla prossima! 👋")
            send_telegram(msg, show_button=False)
            
            # Reset stati
            current_voice_channel = None
            start_time = None

client.run(DISCORD_TOKEN)
