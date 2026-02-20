import discord
from discord.ext import commands
from deep_translator import GoogleTranslator
import re
import os
from flask import Flask
from threading import Thread

# ===== Flask（Render用 keep alive）=====
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# ===== Discord設定 =====
TARGET_CHANNEL_ID = CHANNEL_ID

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def is_english(text: str) -> bool:
    return bool(re.search(r"[a-zA-Z]", text))

def is_japanese(text: str) -> bool:
    return bool(re.search(r"[ぁ-んァ-ン一-龥]", text))

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if message.channel.id != TARGET_CHANNEL_ID:
        return

    content = message.content

    if is_japanese(content):
        translated = GoogleTranslator(source="ja", target="en").translate(content)
        await message.reply(translated)

    elif is_english(content):
        translated = GoogleTranslator(source="en", target="ja").translate(content)
        await message.reply(translated)

    await bot.process_commands(message)

keep_alive()
bot.run(os.environ["TOKEN"])

