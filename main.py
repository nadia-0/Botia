import signal
import discord
import os
import sqlite3
import random
import string
import subprocess, time
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="bt", intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)

# TODO: Find a way to auto populate thsee OR get global commands working
guild_ids = [781590063653191701, 456602312920530945,
             621888002804678656, 822957712241066024, 879355746427474010]
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


@slash.slash(
    name="ping",
    description="Do it >:)",
    guild_ids=guild_ids)
async def _ping(ctx):
    await ctx.send(f"Pong! ({round(bot.latency*1000)}ms)")


@slash.slash(
    name='diceroll',
    description='rolls a die of your choosing',
    guild_ids=guild_ids
)
async def _diceroll(ctx, sides:int):
    if sides <= 1:
        await ctx.send(f"You silly, you can't roll a {sides} sided die!")
    else:
        await ctx.send(f"You rolled a {random.randint(1, sides)} on a {sides} sided die!")


@slash.slash(
    name='coinflip',
    description='flips a coin',
    guild_ids=guild_ids
)
async def _coinflip(ctx):
    if random.randint(1,2) == 1:
        await ctx.send("You flipped heads!")
    else:
        await ctx.send("You flipped tails!")


@slash.slash(
    name='bottom',
    description='alnskjdfnaljkhalskjg',
    guild_ids=guild_ids,
    options=[
        create_option(
            name="option",
            description="choose your bottomness",
            required=True,
            option_type=3,
            choices=[
                create_choice(
                    name="lower case",
                    value="lower"
                ),
                create_choice(
                    name="upper case",
                    value="upper"
                )
            ]
        )
    ]
)
async def _bottomSpeak(ctx, option:str):
    if option == "lower":
        await ctx.send( ''.join(random.choice(string.ascii_lowercase) for i in range(random.randint(6,50))))
    elif option == "upper":
        await ctx.send( ''.join(random.choice(string.ascii_uppercase) for i in range(random.randint(6,50))))


@slash.slash(
    name="gif",
    description="funy gifs :)",
    guild_ids=guild_ids,
    options=[
        create_option(
            name="option",
            description="choose a gif",
            required=True,
            option_type=3,
            choices=[
                create_choice(
                    name="boobs",
                    value="boobs"
                ),
                create_choice(
                    name="piss",
                    value="piss"
                ),
                create_choice(
                    name="weeks",
                    value="weeks"
                )
            ]
        )
    ]
)
async def _gif(ctx, option:str):
    if option == "boobs":
        await ctx.send("https://tenor.com/view/fnaf-boobs-sexy-gif-18802882")
    elif option == "piss":
        await ctx.send("https://tenor.com/view/piss-cop-funny-tonight-sir-gif-22975350")
    elif option == "weeks":
        await ctx.send("https://tenor.com/view/couple-of-weeks-shanese-60days-in-few-weeks-several-weeks-gif-16956066")


# region Mafia-specific
@slash.slash(
    name="quote",
    description="Gives a random quote from the Art of War",
    guild_ids=mafia_id
)
async def _quote(ctx):
    c.execute('SELECT * FROM QUOTES ORDER BY RANDOM() LIMIT 1')
    data = c.fetchall()
    for row in data:
        await ctx.send(row[0] + ' -' + row[1])
        
        
# TODO: make a command that reads the amount of people in a vc and if it's >=8, start the server
# @slash.slash(name='scp',
#              description='CLASS D CLASS D CLASS D CLASS D',
#              guild_ids=mafia_id,
#              options=[
#                  create_option(
#                      name="option",
#                      description="What command?",
#                      required=True,
#                      option_type=3,
#                      choices=[
#                          create_choice(
#                              name="Start",
#                              value="start"
#                          ),
#                          create_choice(
#                              name="Stop",
#                              value="stop"
#                          )
#                      ]
#                  )
#              ])
# async def _scp(ctx, option: str):
#     if option == "start":
#         await ctx.send("Updating the server, please wait...")
#         subprocess.call(["E:\\Games\\steamcmd\\steamcmd.exe", "+@sSteamCmdForcePlatformType windows",
#                         "+login anonymous", "+app_update 996560" "+beta publicbeta", "validate", "+quit"])
#         os.chdir(
#             "E:\\Games\\steamcmd\\steamapps\\common\\SCP Secret Laboratory Dedicated Server")
#         server = subprocess.Popen(
#             ["E:\\Games\\steamcmd\\steamapps\\common\\SCP Secret Laboratory Dedicated Server\\LocalAdmin.exe", "7777"])
#         time.sleep(7.5)
#         servPID = server.pid
#         await ctx.send("Started")
#     else:
#         os.kill(servPID, signal.CTRL_C_EVENT)
#         await ctx.send("Stopped the server")

    
# endregion


bot.run(TOKEN)
