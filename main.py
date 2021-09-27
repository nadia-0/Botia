import discord, os, sys, sqlite3, time, datetime, random
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix="bt", intents=discord.Intents.all())
slash = SlashCommand(bot)
guild_ids = [781590063653191701, 456602312920530945, 621888002804678656]
mafia_id = [781590063653191701, 456602312920530945]

conn = sqlite3.connect('quotes.db')
c = conn.cursor()


@bot.event
async def on_ready():
    guild_count = 0
    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count += 1
    print(f"{bot.user.name} is in {str(guild_count)} servers.")
    print(f"{bot.user.name}\'s id is {bot.user.id}")


@slash.slash(name="ping",
             description="Do it >:)",
             guild_ids=guild_ids)
async def _ping(ctx):
    await ctx.send(f"Pong! ({round(bot.latency*1000)}ms)")

# region Mafia-specific
@slash.slash(name="quote",
             description="Gives a random quote from the Art of War",
             guild_ids=mafia_id)
async def _quote(ctx):
    c.execute('SELECT * FROM QUOTES ORDER BY RANDOM() LIMIT 1')
    data = c.fetchall()
    for row in data:
        await ctx.send(row[0] + ' -' + row[1])


# endregion

bot.run(TOKEN)
