import discord, os, sys
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from dotenv import load_dotenv
from dotenv.compat import to_env

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix="aow!", intents=discord.Intents.all())

slash = SlashCommand(bot, sync_commands=True)
guild_ids = [781590063653191701]

@bot.event
async def on_ready():
    guild_count = 0
    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count += 1
    print(f"{bot.user.name} is in {str(guild_count)} servers.")
    print(f"{bot.user.name}\'s id is {bot.user.id}")

@slash.slash(name="ping", guild_ids=guild_ids)
async def _ping(ctx):
    await ctx.send(f"Pong! ({round(bot.latency*1000)}ms)")


@slash.slash(name="",
             description="",
             guild_ids=guild_ids
             )
async def _quote(ctx, msg):
    await ctx.send("Hello, world!")

bot.run(TOKEN)