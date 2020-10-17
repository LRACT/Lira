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
	async def warn(self, ctx, member: discord.Member, *, reason: typing.Optional[str] = "사유 없음."):
		await ctx.message.delete()
		role = discord.utils.get(ctx.guild.roles, id=711753639722745896)
		if role not in member.roles:
			conn = sqlite3.connect('discord.sqlite')
			cur = conn.cursor()
			cur.execute(f"INSERT INTO infractions(user, reason) VALUES({member.id}, '{reason}')")
			conn.commit()
			conn.close()
			embed = discord.Embed(description=f"사유 : {reason}", color=0x5AFF53)
			embed.set_author(name=f"{str(member)}님이 관리자에게 경고를 받으셨어요.", icon_url=member.avatar_url_as(static_format='png', size=2048))
			dev = self.bot.get_user(526958314647453706)
			embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format='png', size=2048))
		else:
			embed = discord.Embed(description="서버 관리자에 대해서 해당 기능은 비활성화 되어 있어요.", color=0xFF5F5F)
			dev = self.bot.get_user(526958314647453706)
			embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format='png', size=2048))
		await ctx.send(embed=embed)
	
	@commands.command(aliases=["warns"])
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
	async def kick(self, ctx, member: discord.Member, *, reason: typing.Optional[str] = "사유 없음."):
		await ctx.message.delete()
		role = discord.utils.get(ctx.guild.roles, id=711753639722745896)
		if role not in member.roles:
			await ctx.guild.kick(member, reason=reason)
			embed = discord.Embed(description=f"사유 : {reason}", color=0x5AFF53)
			embed.set_author(name=f"{str(member)}님을 서버에서 추방했어요.", icon_url=member.avatar_url_as(static_format='png', size=2048))
			dev = self.bot.get_user(526958314647453706)
			embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format='png', size=2048))
		else:
			embed = discord.Embed(description="서버 관리자에 대해서 해당 기능은 비활성화 되어 있어요.", color=0xFF5F5F)
			dev = self.bot.get_user(526958314647453706)
			embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format='png', size=2048))
		await ctx.send(embed=embed)
	
	@commands.command()
	@commands.has_role(711753639722745896)
	async def slowmode(self, ctx, *args):
		await ctx.message.delete()
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
	async def ban(self, ctx, member: discord.Member, delete: typing.Optional[int] = 0, *, reason: typing.Optional[str] = "사유 없음."):
		await ctx.message.delete()
		role = discord.utils.get(ctx.guild.roles, id=711753639722745896)
		if role not in member.roles:
			await ctx.guild.ban(member, delete_message_days=delete, reason=reason)
			embed = discord.Embed(description=f"사유 : {reason}, {delete}일 간의 메시지가 삭제되었어요.", color=0x5AFF53)
			embed.set_author(name=f"{str(member)}님을 서버에서 영구적으로 차단했어요.", icon_url=member.avatar_url_as(static_format='png', size=2048))
			dev = self.bot.get_user(526958314647453706)
			embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format='png', size=2048))
		else:
			embed = discord.Embed(description="서버 관리자에 대해서 해당 기능은 비활성화 되어 있어요.", color=0xFF5F5F)
			dev = self.bot.get_user(526958314647453706)
			embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format='png', size=2048))
		await ctx.send(embed=embed)
	
	@commands.command()
	@commands.has_role(711753639722745896)
	async def purge(self, ctx, number: int):
		if number > 0 and number <= 100:
			await ctx.message.delete()
			removed = await ctx.channel.purge(limit=number)
			await ctx.send(f":wastebasket: {ctx.author.mention} - 메시지 **{len(removed)}**개를 삭제했어요.", delete_after=10)
	
	@commands.command()
	@commands.has_role(711753639722745896)
	async def mute(self, ctx, member: discord.Member, timeout: typing.Optional[int] = 0, *, reason: typing.Optional[str] = "사유 없음."):
		await ctx.message.delete()
		role = discord.utils.get(ctx.guild.roles, id=711753639722745896)
		if role not in member.roles:
			muted = discord.utils.get(ctx.guild.roles, id=712106679331717141)
			if muted not in member.roles:
				if timeout == 0:
					embed = discord.Embed(description=f"사유 : {reason}\n타임아웃 시간 : 영구적!", color=0x5AFF53)
				else:
					embed = discord.Embed(description=f"사유 : {reason}\n타임아웃 시간 : `{timeout}`초\n \n*주의하세요! 뮤트 중에 봇이 재시작되면 타임아웃이 만료되어요.*", color=0x5AFF53)
				await member.add_roles(muted, reason=reason)
				embed.set_author(name=f"{str(member)}님의 채팅을 차단했어요.", icon_url=member.avatar_url_as(static_format='png', size=2048))
				dev = self.bot.get_user(526958314647453706)
				embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format='png', size=2048))
				if timeout != 0:
					await asyncio.sleep(timeout)
					await member.remove_roles(muted, reason="타임아웃 시간 종료")
					embed = discord.Embed(description=f"사유 : 타임아웃 시간 종료", color=0x5AFF53)
					embed.set_author(name=f"{str(member)}님의 채팅 금지 조치를 해제했어요.", icon_url=member.avatar_url_as(static_format='png', size=2048))
					dev = self.bot.get_user(526958314647453706)
					embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format='png', size=2048))
			else:
				embed = discord.Embed(description="해당 유저의 채팅은 이미 차단되어 있어요.", color=0xFF5F5F)
				dev = self.bot.get_user(526958314647453706)
				embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format='png', size=2048))
		else:
			embed = discord.Embed(description="서버 관리자에 대해서 해당 기능은 비활성화 되어 있어요.", color=0xFF5F5F)
			dev = self.bot.get_user(526958314647453706)
			embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format='png', size=2048))
		await ctx.send(embed=embed)
	
	@commands.command()
	@commands.has_role(711753639722745896)
	async def unmute(self, ctx, member: discord.Member, *, reason: typing.Optional[str] = "사유 없음."):
		await ctx.message.delete()
		muted = discord.utils.get(ctx.guild.roles, id=712106679331717141)
		if muted in member.roles:
			await member.remove_roles(muted, reason=reason)
			embed = discord.Embed(description=f"사유 : {reason}", color=0x5AFF53)
			embed.set_author(name=f"{str(member)}님의 채팅 금지 조치를 해제했어요.", icon_url=member.avatar_url_as(static_format='png', size=2048))
			dev = self.bot.get_user(526958314647453706)
			embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format='png', size=2048))
			await ctx.message.delete()
		else:
			embed = discord.Embed(description="채팅 금지 조치가 적용되지 않은 유저에요.", color=0xFF5F5F)
			dev = self.bot.get_user(526958314647453706)
			embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format='png', size=2048))
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(moderation(bot))
