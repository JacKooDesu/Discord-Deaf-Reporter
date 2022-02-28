import re
import discord
# client 是我們與 Discord 連結的橋樑
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

# 調用 event 函式庫


@client.event
# 當機器人完成啟動時
async def on_ready():
    print('目前登入身份：', client.user)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('-repMute'):
        temp = message.content.split(" ", 2)
        guild = message.guild
        reporter = message.author

        if len(temp) == 1:
            await message.channel.send("未知指令")
        else:
            userId = int(re.sub("\D", "", temp[1]))
            reportMember = guild.get_member(userId)

            if (reportMember.voice is None) or (not reportMember.voice.self_deaf):
                await reporter.move_to(None, reason="胡亂舉報")
                await message.channel.send(f"{reporter.mention} 因胡亂舉報 {reportMember.mention} 而被從語音頻道踢出。")
            else:
                await reportMember.move_to(None, reason="語音頻道內消音")
                await message.channel.send(f"{reportMember.mention} 因在語音頻道內關耳機而被踢出。")

    # if message.content == 'ping':
    #     await message.channel.send('pong')


client.run('OTQ3ODU0NjAwODM5NTE2MjYw.YhzUYw.26wpevvmghqYPUem8POxxRj5raM')
