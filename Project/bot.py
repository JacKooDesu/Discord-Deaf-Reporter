import discord
from discord.ext import commands
from discord.utils import get
import json
import os

path = os.path.dirname(os.path.abspath(__file__))
config = ""
with open(os.path.join(path, "config.json"), "r", encoding="utf8") as file:
    config = json.load(file)

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
client = commands.Bot(
    intents=intents, command_prefix="-report ", case_insensitive=True)


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


@client.command(name='load')
async def load(ctx, extension):
    client.load_extension(f'cmds.{extension}')
    await ctx.send(f'{extension} 加載完成')


@client.command(name='reload')
async def reload(ctx, extension):
    client.reload_extension(f'cmds.{extension}')
    await ctx.send(f'{extension} 重載完成')


@client.command(name='unload')
async def unload(ctx, extension):
    client.unload_extension(f'cmds.{extension}')
    await ctx.send(f'{extension} 卸載完成')

for f in os.listdir(os.path.join(path, 'cmds')):
    if f.endswith('.py'):
        client.load_extension(f'cmds.{f[:-3]}')

client.run(config['token'])
