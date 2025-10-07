import discord
from discord.ext import commands
import os

# Variabili d'ambiente su Railway (NON hardcode)
TOKEN = os.getenv("DISCORD_TOKEN")
USER_ID = int(os.getenv("USER_ID"))

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True
intents.messages = True
intents.dm_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot connesso come {bot.user}")

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        user = await bot.fetch_user(USER_ID)
        await user.send(f"🔔 {member.name} è entrato nel canale vocale: {after.channel.name}")

bot.run(TOKEN)
