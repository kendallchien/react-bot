import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

# LOAD .ENV FILE
load_dotenv()

# GRAB API TOKEN FROM .ENV
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

cogs: list = [
    "cogs.fun",
    "cogs.louvre",
    "cogs.league",
    "cogs.spoiler_chats",
    "cogs.reports"
]

# SET BOT COMMAND PREFIX
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready() -> None:
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

async def main():
    try:
        await bot.start(TOKEN)
    except KeyboardInterrupt:
        pass
    finally:
        await bot.close()
        print("Mecha rin offline")

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
