import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

# LOAD .ENV FILE
load_dotenv()

# GRAB API TOKEN FROM .ENV
TOKEN = os.getenv('DISCORD_TOKEN')
# TOKEN = os.getenv('DISCORD_TOKEN_TEST')
# GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

cogs: list = [
    "cogs.fun",
    "cogs.louvre",
    "cogs.league"
    ]

# SET BOT COMMAND PREFIX
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready() -> None:
    # for guild in bot.guilds:
    #         if guild.name == GUILD:
    #             break
    await bot.change_presence(status=discord.Status.online)
    for cog in cogs:
        try:
            print(f"Loading cog {cog}")
            await bot.load_extension(cog)
            print(f"Loaded cog {cog}")

        except Exception as e:
            exc = "{}: {}".format(type(e).__name__, e)
            print("Failed to load cog {}\n{}".format(cog, exc))

    print('We have logged in as {0.user}'.format(bot))
    # print('Joining {0.id}'.format(guild))

bot.run(TOKEN)
