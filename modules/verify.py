import discord
from discord.ext import commands
import sqlite3
from captcha.image import ImageCaptcha
import asyncio
import random

class auth(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    async def verify(self, ctx):
        role = ctx.guild.get_role(728488298062020609)
        if role is not None and role not in ctx.author.roles:
            await ctx.message.delete()
            img = ImageCaptcha()
            a = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
            random.shuffle(a)
            code = "".join(a)[:6]
            img.write(code, f"temp/{ctx.author.id}.png")
            m = await ctx.send(f":stopwatch: {ctx.author.mention} - 60초 안에 보안 코드를 입력해주세요.", file=discord.File(f"temp/{ctx.author.id}.png"))
            def check(msg):
                return msg.channel == ctx.channel and msg.author == ctx.author
            try:
                msg = await self.bot.wait_for("message", timeout=60, check=check)
            except asyncio.TimeoutError:
                await m.edit(content=f"<:cs_no:659355468816187405> {ctx.author.mention} - 인증 시간이 초과되었어요.")
                await asyncio.sleep(3)
                await m.delete()
            else:
                await msg.delete()
                await m.delete()
                if msg.content == code:
                    m2 = await ctx.send(content=f"<:cs_yes:659355468715786262> {ctx.author.mention} - 인증이 완료되셨어요. 곧 역할이 자동으로 지급되실 거에요.")
                    await ctx.author.add_roles(role)
                    await asyncio.sleep(3)
                    await m2.delete()
                else:
                    m2 = await ctx.send(f"<:cs_protect:659355468891947008> {ctx.author.mention} - 코드가 잘못되었어요.\n잠시 후 인증을 다시 시도해주세요.")
                    await asyncio.sleep(3)
                    await m2.delete()
        else:
            await ctx.send(f"<:cs_id:659355469034422282> {ctx.author.mention} - 이미 역할을 가지고 계셔서 취소되었어요.")

def setup(bot):
    bot.add_cog(auth(bot))
