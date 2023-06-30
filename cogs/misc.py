import yaml
from dotenv import load_dotenv
from discord.ext import commands

with open('img.yaml') as f:

    data = yaml.load(f, Loader=yaml.FullLoader)


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Fun(bot))