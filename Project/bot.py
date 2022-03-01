import re
from sys import prefix
import discord
from discord.ext import commands
from discord.utils import get
import json
import os

path = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(path, "config.json"), "r", encoding="utf8") as file:
    config = json.load(file)

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
client = commands.Bot(
    intents=intents, command_prefix="-report ", case_insensitive=True)


@client.command(name='deaf')
async def deaf(ctx, targetId: str):
    if ctx.author == client.user:
        return

    guild = ctx.guild
    reporter = ctx.author

    userId = int(re.sub("\D", "", targetId))
    reportMember = guild.get_member(userId)

    if (reportMember.voice is None) or (not reportMember.voice.self_deaf):
        await reporter.move_to(None, reason="胡亂舉報")
        await ctx.channel.send(f"{reporter.mention} 因胡亂舉報 {reportMember.mention} 而被從語音頻道踢出。")
    else:
        await reportMember.move_to(None, reason="語音頻道內消音")
        await ctx.channel.send(f"{reportMember.mention} 因在語音頻道內關耳機而被踢出。")


@client.command(name='disgustingSetup')
async def disgustingSetup(ctx):
    guild = ctx.guild
    with open(os.path.join(path, "disgusting.png"), 'rb') as fd:
        await guild.create_custom_emoji(name='DisgustingReaction', image=fd.read())


@client.event
async def on_ready():
    print('目前登入身份：', client.user)


@client.event
async def on_raw_reaction_add(payload):
    emoji = payload.emoji
    if emoji.name != 'DisgustingReaction':
        return

    textChannel = client.get_channel(payload.channel_id)
    msg = await textChannel.fetch_message(payload.message_id)
    reaction = get(msg.reactions, emoji=payload.emoji)
    if len(msg.attachments) == 0:
        return

    if reaction and reaction.count >= config['disgustingCount']:
        await msg.delete()
        await textChannel.send(f"因為 {msg.author.mention} 的訊息過激，已被刪除。")

client.run(config['token'])
