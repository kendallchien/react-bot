import discord
import numpy as np
import os
import asyncio
import random
import yaml
import time
from dotenv import load_dotenv
from discord.ext import commands
from discord.ui import Button, View
from datetime import datetime
import pandas as pd

with open('img.yaml') as f:

    data = yaml.load(f, Loader=yaml.FullLoader)


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Fun(bot))