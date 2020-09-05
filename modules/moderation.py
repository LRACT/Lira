import discord
from discord.ext import commands
import sqlite3
import typing
import asyncio

class moderation(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.has_role(711753639722745896)
	async def warn(self, ctx, member: discord.Member):
		queue = ctx.message.content.split(" ")[2:]
		if not queue:
			reason = '사유 없음.'
		else:
			reason = ""
			for a in queue:
				reason += f"{a} "
		role = discord.utils.get(ctx.guild.roles, id=711753639722745896)
		botrole = discord.utils.get(ctx.guild.roles, id=712199886518616074)
		if role not in member.roles and botrole not in member.roles:
			conn = sqlite3.connect('discord.sqlite')
			cur = conn.cursor()
			cur.execute(f"INSERT INTO infractions(user, reason) VALUES({member.id}, '{reason}')")
			conn.commit()
			conn.close()
			embed = discord.Embed(description=f"사유 : {reason}", color=0xFFFCC9)
			embed.set_author(name=f"{str(member)}님에게 경고를 주었어요.", icon_url=member.avatar_url_as(static_format='png', size=2048))
			dev = self.bot.get_user(526958314647453706)
			embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format='png', size=2048))
			await ctx.message.delete()
			await ctx.send(ctx.author.mention, embed=embed)
		else:
			embed = discord.Embed(description="관리자 및 서버 관리 봇에게 경고를 줄 수 없어요!", color=0xFF5F5F)
			dev = self.bot.get_user(526958314647453706)
			embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format='png', size=2048))
			await ctx.send(ctx.author.mention, embed=embed)
	
	@commands.command()
	async def infractions(self, ctx, member: discord.Member):
		conn = sqlite3.connect('discord.sqlite')
		cur = conn.cursor()
		cur.execute(f"SELECT * FROM infractions WHERE user = {member.id}")
		rows = cur.fetchall()
		if not rows:
			embed = discord.Embed(description=f"*(표시할 내용 없음)*", color=0xFFFCC9)
			embed.set_author(name=f"{str(member)}님은 경고를  가지고 있지 않아요.", icon_url=member.avatar_url_as(static_format='png', size=2048))
			dev = self.bot.get_user(526958314647453706)
			embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format='png', size=2048))
			await ctx.send(ctx.author.mention, embed=embed)
		else:
			a = ""
			i = 1
			for row in rows:
				a += f"#{i} :: {row[1]}\n"
				i += 1
			embed = discord.Embed(description=f"경고 목록 : \n{a}", color=0xFFFCC9)
			embed.set_author(name=f"{str(member)}님은 총 {len(rows)}개의 경고를 가지고 있어요.", icon_url=member.avatar_url_as(static_format='png', size=2048))
			dev = self.bot.get_user(526958314647453706)
			embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format='png', size=2048))
			await ctx.send(ctx.author.mention, embed=embed)
	
	@commands.command()
	@commands.has_role(711753639722745896)
	async def kick(self, ctx, member: discord.Member):
		queue = ctx.message.content.split(" ")[2:]
		if not queue:
			reason = '사유 없음.'
		else:
			reason = ""
			for a in queue:
				reason += f"{a} "
		role = discord.utils.get(ctx.guild.roles, id=711753639722745896)
		botrole = discord.utils.get(ctx.guild.roles, id=712199886518616074)
		if role not in member.roles and botrole not in member.roles:
			await ctx.guild.kick(member, reason=reason)
			embed = discord.Embed(description=f"사유 : {reason}", color=0xAFFDEF)
			embed.set_author(name=f"{str(member)}님을 서버에서 추방했어요.", icon_url=member.avatar_url_as(static_format='png', size=2048))
			dev = self.bot.get_user(526958314647453706)
			embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format='png', size=2048))
			await ctx.message.delete()
			await ctx.send(ctx.author.mention, embed=embed)
		else:
			embed = discord.Embed(description="관리자 및 서버 관리 봇을 서버에서 추방할 수 없어요!", color=0xFF5F5F)
			dev = self.bot.get_user(526958314647453706)
			embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format='png', size=2048))
			await ctx.send(ctx.author.mention, embed=embed)
	
	@commands.command()
	@commands.has_role(711753639722745896)
	async def slowmode(self, ctx, *args):
		if not args:
			dev = self.bot.get_user(526958314647453706)
			embed = discord.Embed(title="잘못된 명령어 사용법", description=f"이 명령어에 반드시 필요한 아래 내용이 없어요.\n \n`delay`", color=0xFF0000)
			embed.set_author(name="Traceback", icon_url=self.bot.user.avatar_url_as(static_format="png", size=2048))
			embed.set_footer(text=f"Powered by {dev.name}#{dev.discriminator}", icon_url=dev.avatar_url_as(static_format="png", size=2048))
			embed.set_thumbnail(url=ctx.author.avatar_url_as(static_format="png", size=2048))
			await ctx.send(embed=embed)
		else:
			if args[0].isdecimal() == True:
				if int(args[0]) <= 21600 and int(args[0]) > 0:
					await ctx.channel.edit(slowmode_delay=int(args[0]))
					await ctx.send(f":stopwatch: {ctx.author.mention} - <#{ctx.channel.id}> 채널을 *느 리 게  만 들 었 어 요 .*\n이제 서버 관리자를 제외한 모든 유저들은 {args[0]}초에 한 번만 메시지를 보낼 수 있어요.\n \n*메시지 딜레이를 비활성화 하시려면 `r.slowmode off` 명령어를 사용해주세요.*")
				else:
					await ctx.send(f":no_entry_sign: {ctx.author.mention} - 범위가 잘못되었어요. 1 - 21600 사이의 정수를 입력해주세요.")
			else:
				if args[0] == 'off':
					if ctx.channel.slowmode_delay != 0:
						await ctx.channel.edit(slowmode_delay=0)
						await ctx.send(f":stopwatch: {ctx.author.mention} - 채널의 메시지 딜레이를 해제했어요!")
					else:
						await ctx.send(f":no_entry_sign: {ctx.author.mention} - 이 채널은 이미 메시지 딜레이가 없어요.")
				else:
					await ctx.send(f":no_entry_sign: {ctx.author.mention} - 잘못된 명령어 사용이에요. 이 명령어에는 1 - 21600 사이의 정수 혹은 `off`만 사용할 수 있어요.")

	@commands.command()
	@commands.has_role(711753639722745896)
	async def ban(self, ctx, member: discord.Member, delete: typing.Optional[int] = 0):
		if ctx.message.content.split(" ")[2:]:
			if ctx.message.content.split(" ")[2].isdecimal() == True:
				queue = ctx.message.content.split(" ")[3:]
			else:
				queue = ctx.message.content.split(" ")[2:]
			reason = ""
			for a in queue:
				reason += f"{a} "
		else:
			reason = "사유 없음."
                        
		role = discord.utils.get(ctx.guild.roles, id=711753639722745896)
		botrole = discord.utils.get(ctx.guild.roles, id=712199886518616074)
		if role not in member.roles and botrole not in member.roles:
			await ctx.guild.ban(member, delete_message_days=delete, reason=reason)
			embed = discord.Embed(description=f"사유 : {reason}, {delete}일 간의 메시지가 삭제되었어요.", color=0xC0FA1B)
			embed.set_author(name=f"{str(member)}님을 서버에서 영구적으로 차단했어요.", icon_url=member.avatar_url_as(static_format='png', size=2048))
			dev = self.bot.get_user(526958314647453706)
			embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format='png', size=2048))
			await ctx.message.delete()
			await ctx.send(ctx.author.mention, embed=embed)
		else:
			embed = discord.Embed(description="관리자 및 서버 관리 봇을 서버에서 차단할 수 없어요!", color=0xFF5F5F)
			dev = self.bot.get_user(526958314647453706)
			embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format='png', size=2048))
			await ctx.send(ctx.author.mention, embed=embed)
	
	@commands.command()
	@commands.has_role(711753639722745896)
	async def purge(self, ctx, *args):
		if args:
			if args[0].isdecimal() == True:
				if int(args[0]) > 0:
					if int(args[0]) <= 100:
						await ctx.message.delete()
						await ctx.channel.purge(limit=int(args[0]))
						await ctx.send(f":wastebasket: {ctx.author.mention} - 메시지 **{args[0]}**개를 삭제했어요.", delete_after=10)
	
	@commands.command()
	@commands.has_role(711753639722745896)
	async def mute(self, ctx, member: discord.Member, timeout: typing.Optional[int] = 0):
		if timeout != 0:
			queue = ctx.message.content.split(" ")[3:]
		else:
			queue = ctx.message.content.split(" ")[2:]
		if not queue:
			reason = '사유 없음.'
		else:
			reason = ""
			for a in queue:
				reason += f"{a} "
		await ctx.message.delete()
		role = discord.utils.get(ctx.guild.roles, id=711753639722745896)
		botrole = discord.utils.get(ctx.guild.roles, id=712199886518616074)
		if role not in member.roles and botrole not in member.roles:
			muted = discord.utils.get(ctx.guild.roles, id=712106679331717141)
			if muted not in member.roles:
				if timeout == 0:
					embed = discord.Embed(description=f"사유 : {reason}\n타임아웃 시간 : 영구적!\n \n*주의하세요! 봇이 재시작될 경우 타임아웃이 취소되고, 영구적으로 뮤트되어요.*", color=0xFFFCC9)
				else:
					embed = discord.Embed(description=f"사유 : {reason}\n타임아웃 시간 : `{timeout}`초\n \n*주의하세요! 봇이 재시작될 경우 타임아웃이 취소되고, 영구적으로 뮤트되어요.*", color=0xFFFCC9)
				await member.add_roles(muted, reason=reason)
				embed.set_author(name=f"{str(member)}님의 채팅을 차단했어요.", icon_url=member.avatar_url_as(static_format='png', size=2048))
				dev = self.bot.get_user(526958314647453706)
				embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format='png', size=2048))
				await ctx.send(ctx.author.mention, embed=embed)
				if timeout != 0:
					await asyncio.sleep(timeout)
					await member.remove_roles(muted, reason="타임아웃 시간 종료")
					embed = discord.Embed(description=f"사유 : 타임아웃 시간 종료", color=0xC0FA1B)
					embed.set_author(name=f"{str(member)}님의 채팅 금지 조치를 해제했어요.", icon_url=member.avatar_url_as(static_format='png', size=2048))
					dev = self.bot.get_user(526958314647453706)
					embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format='png', size=2048))
					await ctx.send(embed=embed)
			else:
				embed = discord.Embed(description="해당 유저의 채팅은 이미 차단되어 있어요.", color=0xFF5F5F)
				dev = self.bot.get_user(526958314647453706)
				embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format='png', size=2048))
				await ctx.send(ctx.author.mention, embed=embed)
		else:
			embed = discord.Embed(description="관리자 및 서버 관리 봇의 채팅을 제한할 수 없어요!", color=0xFF5F5F)
			dev = self.bot.get_user(526958314647453706)
			embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format='png', size=2048))
			await ctx.send(ctx.author.mention, embed=embed)
	
	@commands.command()
	@commands.has_role(711753639722745896)
	async def unmute(self, ctx, member: discord.Member):
		queue = ctx.message.content.split(" ")[2:]
		if not queue:
			reason = '사유 없음.'
		else:
			reason = ""
			for a in queue:
				reason += f"{a} "
		muted = discord.utils.get(ctx.guild.roles, id=712106679331717141)
		if muted in member.roles:
			await member.remove_roles(muted, reason=reason)
			embed = discord.Embed(description=f"사유 : {reason}", color=0xC0FA1B)
			embed.set_author(name=f"{str(member)}님의 채팅 금지 조치를 해제했어요.", icon_url=member.avatar_url_as(static_format='png', size=2048))
			dev = self.bot.get_user(526958314647453706)
			embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format='png', size=2048))
			await ctx.message.delete()
			await ctx.send(ctx.author.mention, embed=embed)
		else:
			embed = discord.Embed(description="채팅 금지 조치가 적용되지 않은 유저에요.", color=0xFF5F5F)
			dev = self.bot.get_user(526958314647453706)
			embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format='png', size=2048))
			await ctx.send(ctx.author.mention, embed=embed)

def setup(bot):
	bot.add_cog(moderation(bot))
