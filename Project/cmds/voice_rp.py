import re
from core.cogBase import cog_base
import discord
from discord.ext import commands

class voice_rp(cog_base):
    @commands.command(name='deaf')
    async def deaf(self,ctx, targetId: str):
        if ctx.author == self.bot.user:
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

def setup(bot):
    bot.add_cog(voice_rp(bot))