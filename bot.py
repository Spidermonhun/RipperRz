import os
import re
import asyncio
import aiohttp
import random
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from concurrent.futures import ThreadPoolExecutor

# ---------------- CONFIG -------------------
BOT_TOKEN = os.getenv("BOT_TOKEN", "Your_Token")
OWNER_ID = int(os.getenv("OWNER_ID", 1234567890))
AUTHORIZED = {OWNER_ID}
BANNED_USERS = set()
RAZOR_SITES = ["api.razorpay.com", "x.razorpay.com"]
PROXIES = []
MAX_CONCURRENT_TASKS = 500
RESULT_LOG = []

# Initialize bot
bot = AsyncTeleBot(BOT_TOKEN)

# Regex to match CCs: 4000|01|2030|123
cc_regex = re.compile(r"(\d{15,16})[|/\s](\d{2})[|/\s](\d{4})[|/\s](\d{3,4})")

# Proxy scraper from multiple live sources (no dead shit)
async def fetch_proxies(session: aiohttp.ClientSession):
    global PROXIES
    urls = [
        "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
        "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
        "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=5000&country=all&ssl=all&anonymity=all"
    ]
    PROXIES.clear()
    for url in urls:
        try:
            async with session.get(url) as resp:
                text = await resp.text()
                lines = text.splitlines()
                for line in lines:
                    if ":" in line.strip():
                        proxy = f"http://{line.strip()}"
                        if proxy not in PROXIES:
                            PROXIES.append(proxy)
        except Exception as e:
            continue  # Move on if one source fails

@bot.message_handler(commands=['start'])
async def start(message: Message):
    if message.from_user.id in BANNED_USERS:
        return await bot.reply_to(message, "🖕 You're banned.")
    
    await bot.reply_to(message,
        f"⚡️ **RazorRipper v3 - Online**\n"
        f"🔥 Cards checked: {len(RESULT_LOG)}\n"
        f"🔄 Proxies loaded: {len(PROXIES)}\n"
        f"👑 Owner: `{OWNER_ID}`\n\n"
        "**Commands:** `/mass`, `/clean`, `/split`, `/auth`, `/charged`, `/declined`"
    )

@bot.message_handler(commands=['clean'])
async def clean_cards(message: Message):
    if message.from_user.id not in AUTHORIZED:
        return await bot.reply_to(message, "❌ Not authorized.")

    reply_msg = message.reply_to_message
    if not reply_msg or not reply_msg.document:
        return await bot.reply_to(message, "📎 Reply to a .txt file with /clean")

    file_info = await bot.get_file(reply_msg.document.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    
    raw_data = downloaded_file.decode('utf-8', errors='ignore')
    cleaned_ccs = []
    
    seen_hashes = set()
    
    for line in raw_data.splitlines():
        match = cc_regex.search(line)
        if match:
            cc_full = '|'.join(match.groups())
            card_hash = cc_full[:6] + '|' + cc_full[-4:]  # BIN + last 4
            if card_hash not in seen_hashes:
                seen_hashes.add(card_hash)
                cleaned_ccs.append(cc_full)

    filename_out = f"CLEAN_{reply_msg.document.file_name}"
    
    with open(filename_out, 'w') as f:
        f.write('\n'.join(cleaned_ccs))

    await bot.send_document(
        message.chat.id,
        open(filename_out, 'rb'),
        caption=f"✅ Cleaned → {len(cleaned_ccs)} valid cards (duplicates removed)"
  )
                  
