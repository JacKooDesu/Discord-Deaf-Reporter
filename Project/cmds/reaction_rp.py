from core.cogBase import cog_base
from discord.ext import commands
from datetime import timezone, timedelta
import bot
from discord.utils import get

class reaction_rp(cog_base):
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        emoji = payload.emoji
        if emoji.name != 'DisgustingReaction':
            return

        textChannel = self.bot.get_channel(payload.channel_id)
        if textChannel.name == bot.config['channel']:
            return

        msg = await textChannel.fetch_message(payload.message_id)
        reaction = get(msg.reactions, emoji=payload.emoji)
        if len(msg.attachments) == 0 and len(msg.embeds) == 0:
            return

        if reaction and reaction.count >= bot.config['disgustingCount']:
            channel = get(self.bot.get_guild(
                payload.guild_id).text_channels, name=bot.config['channel'])
            await textChannel.send(f"因為 {msg.author.mention} 的訊息過激，已被刪除並移至 {channel.mention}。")

            utcOffset = timezone(timedelta(hours=bot.config['utcOffset']))
            time = msg.created_at.replace(tzinfo=timezone.utc)
            content = f'{msg.author.mention} 於 {time.astimezone(utcOffset).strftime("%Y-%m-%d %H:%M:%S")}\n' + \
                msg.content

            files = []
            for a in msg.attachments:
                files.append(await a.to_file())
            await channel.send(content, files=files, embed=None if len(msg.embeds) == 0 else msg.embeds[0])
            await msg.delete()

def setup(bot):
    bot.add_cog(reaction_rp(bot))