import re
from sys import prefix
from turtle import position
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


@client.command(name='channelSetup')
async def channelSetup(ctx):
    guild = ctx.guild
    await guild.create_text_channel(config['channel'])


@client.command(name='usage')
async def usage(ctx):
    guild = ctx.guild
    with open(os.path.join(path, "usage.txt"))as f:
        file = f.read()
    disgustingEmoji = get(client.emojis, name='DisgustingReaction')
    file = file.replace(':DisgustingReaction:', str(disgustingEmoji))
    await ctx.send(file)


@client.event
async def on_ready():
    print('目前登入身份：', client.user)


@client.event
async def on_raw_reaction_add(payload):
    emoji = payload.emoji
    if emoji.name != 'DisgustingReaction':
        return

    textChannel = client.get_channel(payload.channel_id)
    if textChannel.name == config['channel']:
        return

    msg = await textChannel.fetch_message(payload.message_id)
    reaction = get(msg.reactions, emoji=payload.emoji)
    if len(msg.attachments) == 0 and len(msg.embeds) == 0:
        return

    if reaction and reaction.count >= config['disgustingCount']:
        channel = get(client.get_guild(
            payload.guild_id).text_channels, name=config['channel'])
        await textChannel.send(f"因為 {msg.author.mention} 的訊息過激，已被刪除並移至 {channel.mention}。")
        content = f'{msg.author.mention} 於 {msg.created_at.strftime("%Y-%m-%d %H:%M:%S")}\n' + msg.content
        files = []
        for a in msg.attachments:
            files.append(await a.to_file())
        await channel.send(content, files=files, embed=None if len(msg.embeds) == 0 else msg.embeds[0])
        await msg.delete()

client.run(config['token'])
