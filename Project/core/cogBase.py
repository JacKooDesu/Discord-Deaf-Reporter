import discord
from discord.ext import commands
import json
import os

path = os.path.dirname(os.path.abspath(__file__))

class cog_base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
