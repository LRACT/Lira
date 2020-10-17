import discord
from discord.ext import commands
import asyncio
import sqlite3
import random
import typing

class level(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.Cog.listener()
	async def on_message(self, msg):
		if msg.author.bot:
			return
		elif msg.channel.type == discord.ChannelType.private:
			return
		elif msg.guild.id != 702880464893116518:
			return
		elif msg.content.startswith("r.") or msg.content.startswith(self.bot.user.mention):
			return
		else:
			conn = sqlite3.connect('discord.sqlite')
			cur = conn.cursor()
			cur.execute(f"SELECT * FROM rank WHERE user = {msg.author.id}")
			rows = cur.fetchall()
			add = random.randint(10, 20)
			if not rows:
				cur.execute(f"INSERT INTO rank(user, exp, level, next, cooldown) VALUES({msg.author.id}, {add}, 0, 300, 'true')")
				conn.commit()
				conn.close()
				await asyncio.sleep(30)
				conn = sqlite3.connect('discord.sqlite')
				cur = conn.cursor()
				cur.execute(f"UPDATE rank SET cooldown = 'false' WHERE user = {msg.author.id}")
				conn.commit()
				conn.close()
			else:
				if rows[0][4] == 'false':
					now_exp = int(rows[0][1]) + add
					if now_exp >= int(rows[0][3]):
						lvl = int(rows[0][2]) + 1
						next_exp = round(now_exp * 1.2)
						cur.execute(f"UPDATE rank SET exp = {now_exp} WHERE user = {msg.author.id}")
						cur.execute(f"UPDATE rank SET level = {lvl} WHERE user = {msg.author.id}")
						cur.execute(f"UPDATE rank SET next = {next_exp} WHERE user = {msg.author.id}")
						cur.execute(f"UPDATE rank SET cooldown = 'true' WHERE user = {msg.author.id}")
						conn.commit()
						conn.close()
						await msg.channel.send(f"축하해요, {msg.author.mention}님! 레벨이 1 오르셨어요! 현재 레벨 : {lvl}")
						await asyncio.sleep(30)
						conn = sqlite3.connect('discord.sqlite')
						cur = conn.cursor()
						cur.execute(f"UPDATE rank SET cooldown = 'false' WHERE user = {msg.author.id}")
						conn.commit()
						conn.close()
					else:
						cur.execute(f"UPDATE rank SET exp = {now_exp} WHERE user = {msg.author.id}")
						cur.execute(f"UPDATE rank SET cooldown = 'true' WHERE user = {msg.author.id}")
						conn.commit()
						conn.close()
						await asyncio.sleep(30)
						conn = sqlite3.connect('discord.sqlite')
						cur = conn.cursor()
						cur.execute(f"UPDATE rank SET cooldown = 'false' WHERE user = {msg.author.id}")
						conn.commit()
						conn.close()

	@commands.command()
	@commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
	async def rank(self, ctx, member: typing.Optional[discord.Member] = None):
		if member is None:
			member = ctx.author
		dev = self.bot.get_user(526958314647453706)
		conn = sqlite3.connect('discord.sqlite')
		cur = conn.cursor()
		cur.execute(f"SELECT * FROM rank WHERE user = {member.id}")
		rows = cur.fetchall()
		if rows:
			embed = discord.Embed(title=f"{str(member)}님의 경험치 정보", description=f"모든 경험치는 1분에 1회만 적립돼요! 경험치에 문제가 있는 것 같나요? 티켓을 열어주세요!", color=0xFFFCC9)
			embed.add_field(name="현재 경험치", value=rows[0][1])
			embed.add_field(name="목표 경험치", value=rows[0][3])
			embed.add_field(name="현재 레벨", value=rows[0][2])
			embed.set_thumbnail(url=member.avatar_url_as(static_format='png', size=2048))
			embed.set_author(name="레벨", icon_url=self.bot.user.avatar_url)
		else:
			embed = discord.Embed(description=f"{str(member)}님은 경험치 정보가 등록되지 않았어요!", color=0xFF5F5F)
		embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format='png', size=2048))
		await ctx.send(ctx.author.mention, embed=embed)

def setup(bot):
	bot.add_cog(level(bot))
