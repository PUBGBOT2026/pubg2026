import os
from threading import Thread

import discord
from discord.ext import commands
from flask import Flask
import requests

# ===========================
# Environment Variables
# ===========================

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
PUBG_API = os.getenv("PUBG_API")

# ===========================
# Discord Bot
# ===========================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ===========================
# Render Web Server
# ===========================

app = Flask(__name__)

@app.route("/")
def home():
    return "PUBG Bot Online"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

Thread(target=run_web).start()

# ===========================
# Ready
# ===========================

@bot.event
async def on_ready():
    print(f"Bejelentkezve: {bot.user}")

# ===========================
# PUBG Command
# ===========================

@bot.command()
async def pubg(ctx, *, player_name):

    headers = {
        "Authorization": f"Bearer {PUBG_API}",
        "Accept": "application/vnd.api+json"
    }

    url = f"https://api.pubg.com/shards/steam/players?filter[playerNames]={player_name}"

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        await ctx.send("❌ A játékos nem található.")
        return

    data = r.json()["data"][0]

    attributes = data["attributes"]

    embed = discord.Embed(
        title=f"🎮 {attributes['name']}",
        color=discord.Color.orange()
    )

    embed.add_field(
        name="Account ID",
        value=data["id"],
        inline=False
    )

    embed.add_field(
        name="Shard",
        value="Steam",
        inline=True
    )

    embed.set_footer(text="PUBG Official API")

    await ctx.send(embed=embed)

# ===========================
# Run
# ===========================

bot.run(DISCORD_TOKEN)
