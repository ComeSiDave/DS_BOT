import discord
from discord.ext import commands
import os
from dotenv import load_dotenv   # pip install python-dotenv

load_dotenv()                    # carica .env se esiste

TOKEN     = os.getenv("DISCORD_TOKEN")
USER_ID   = int(os.getenv("USER_ID"))   # il tuo ID numerico

intents = discord.Intents.default()
intents.voice_states = True
intents.members        = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"✅ Bot connesso come {bot.user} (ID: {bot.user.id})")

@bot.event
async def on_voice_state_update(member, before, after):
    # entra in un canale vocale
    if before.channel is None and after.channel is not None:
        user = await bot.fetch_user(USER_ID)
        await user.send(f"🔔 **{member}** è entrato nel canale vocale **{after.channel.name}**")

@bot.command()
@commands.has_permissions(administrator=True)
async def setvoicechannel(ctx):
    """Imposta il canale corrente come destinazione notifiche vocali."""
    # salva nel dizionario interno (o su file/DB se vuoi persistenza)
    bot.voice_log_channel = ctx.channel.id
    await ctx.send(f"✅ Notifiche vocali inviate qui: {ctx.channel.mention}")

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        cid = getattr(bot, "voice_log_channel", None)
        if cid:
            channel = bot.get_channel(cid)
            if channel:
                await channel.send(f"🔔 **{member}** è entrato nel canale vocale **{after.channel.name}**")

bot.run(TOKEN)