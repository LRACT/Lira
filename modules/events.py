import discord
from discord.ext import commands
import datetime
from pytz import timezone, utc
import sqlite3

class events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print(str(self.bot.user))
		print(self.bot.user.id)
		conn = sqlite3.connect('discord.sqlite')
		cur = conn.cursor()
		cur.execute("SELECT * FROM bot")
		rows = cur.fetchall()
		if rows[0][2] == "온라인 / Online":
			status = discord.Status.online
		elif rows[0][2] == "자리비움 / Idle":
			status = discord.Status.idle
		elif rows[0][2] == "다른 용무 중 / Do not disturb":
			status = discord.Status.do_not_disturb
		elif rows[0][2] == "오프라인 / Offline":
			status = discord.Status.offline
		await self.bot.change_presence(status=status, activity=discord.Game(rows[0][3]))
		print("READY")
		now = datetime.datetime.now()
		cur.execute(f"UPDATE bot SET uptime = '{now}'")
		conn.commit()
		conn.close()

	@commands.Cog.listener()
	async def on_member_join(self, member):
		if member.guild.id == 702880464893116518:
			humans = self.bot.get_channel(713254695363412070)
			bots = self.bot.get_channel(713254625955807243)
			h = 0
			b = 0
			for m in member.guild.members:
				if m.bot:
					b += 1
				else:
					h += 1
			await humans.edit(name=f"멤버 : {h}명")
			await bots.edit(name=f"봇 : {b}개")

			if member.bot:
				bot_role = discord.utils.get(member.guild.roles, id=711775686678937651)
				await member.add_roles(bot_role)
			else:
				#human_role = discord.utils.get(member.guild.roles, id=728488298062020609)
				#await member.add_roles(human_role)
				channel = self.bot.get_channel(711748833402552320)
				await channel.send(f"{member.mention}님이 **{member.guild.name}** 서버에 등장했어요! ㄷㄷㄷㅈ")
				try:
					embed = discord.Embed(description=f"{member.mention}님 어서오세요! **{member.guild.name}** 서버에 오신 것을 환영해요!\n이 서버는 개발자분들과 함께 소통하고, 자신이 막힌 코드에 대해서 질문하실 수 있어요.\n앗, 서버에 대한 문의(Ex: 파트너, 유저 신고 등)를 하고 싶으신가요? <#712260887167107074> 채널에서 `r.new` 명령어를 사용해주세요!", color=0xFFFCC9)
					dev = self.bot.get_user(526958314647453706)
					embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url)
					embed.set_author(name="어서오세요!", icon_url=self.bot.user.avatar_url)
					embed.set_thumbnail(url=member.avatar_url_as(static_format='png', size=2048))
					await member.send(member.mention, embed=embed)
				except:
					print(f"{str(member)} :: Failed to send Direct Message.")

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		if member.guild.id == 702880464893116518:
			humans = self.bot.get_channel(713254695363412070)
			bots = self.bot.get_channel(713254625955807243)
			h = 0
			b = 0
			for m in member.guild.members:
				if m.bot:
					b += 1
				else:
					h += 1
			await humans.edit(name=f"멤버 : {h}명")
			await bots.edit(name=f"봇 : {b}개")

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		message_id = payload.message_id
		if message_id == 750668188932505611:
			guild_id = payload.guild_id
			guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)
			role = None
			if str(payload.emoji) == '<:javascript:750666101599502387>':
				role = discord.utils.get(guild.roles, id=750668383044894780) # js
			if str(payload.emoji) == '<:python:750666101968338944>':
				role = discord.utils.get(guild.roles, id=750668384085213184) # py
			if str(payload.emoji) == '<:csharp:750666101720875040>':
				role = discord.utils.get(guild.roles, id=750668386673098858) # C
			if str(payload.emoji) == '<:java:751427083963727962>':
				role = discord.utils.get(guild.roles, id=750668381170171904) # java
			if role is not None:
				member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
				if member is not None:
					await member.add_roles(role)

	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, payload):
		message_id = payload.message_id
		if message_id == 750668188932505611:
			guild_id = payload.guild_id
			guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)
			role = None
			if str(payload.emoji) == '<:javascript:750666101599502387>':
				role = discord.utils.get(guild.roles, id=750668383044894780) # js
			if str(payload.emoji) == '<:python:750666101968338944>':
				role = discord.utils.get(guild.roles, id=750668384085213184) # py
			if str(payload.emoji) == '<:csharp:750666101720875040>':
				role = discord.utils.get(guild.roles, id=750668386673098858) # C
			if str(payload.emoji) == '<:java:751427083963727962>':
				role = discord.utils.get(guild.roles, id=750668381170171904) # java
			if role is not None:
				member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
				if member is not None:
					await member.remove_roles(role)

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		dev = self.bot.get_user(526958314647453706)
		if isinstance(error, commands.CommandNotFound):
			await ctx.send(f'{ctx.author.mention} - Unknown command. Type "r.help" for help.')
		elif isinstance(error, commands.NotOwner):
			await ctx.send(f"{ctx.author.mention} - I'm sorry, but you do not have permission to perform this command. Please contact server administrators if you believe that this is in error.")
		elif isinstance(error, commands.MissingRole):
			#embed = discord.Embed(title="역할 찾지 못함", description=f"이 명령어를 사용하려면 아래 역할이 필요해요.\n \n<@&{error.missing_role}>", color=0xAFFDEF)
			#embed.set_author(name="Traceback", icon_url=self.bot.user.avatar_url_as(static_format="png", size=2048))
			#embed.set_footer(text=f"Powered by {dev.name}#{dev.discriminator}", icon_url=dev.avatar_url_as(static_format="png", size=2048))
			#embed.set_thumbnail(url=ctx.author.avatar_url_as(static_format="png", size=2048))
			#await ctx.send(embed=embed)
			await ctx.send(f"{ctx.author.mention} - I'm sorry, but you do not have permission to perform this command. Please contact server administrators if you believe that this is in error.")
		elif isinstance(error, commands.CommandOnCooldown):
			embed = discord.Embed(title="커맨드 쿨다운", description=f"이 명령어를 다시 사용하기 위해 {round(error.retry_after)}초를 더 기다리셔야 해요!", color=0xAFFDEF)
			embed.set_author(name="Traceback", icon_url=self.bot.user.avatar_url_as(static_format="png", size=2048))
			embed.set_footer(text=f"Powered by {dev.name}#{dev.discriminator}", icon_url=dev.avatar_url_as(static_format="png", size=2048))
			embed.set_thumbnail(url=ctx.author.avatar_url_as(static_format="png", size=2048))
			await ctx.send(embed=embed)
		elif isinstance(error, commands.MissingRequiredArgument):
			embed = discord.Embed(title="내용 부족", description=f"아래 내용이 없어 명령어를 실행하지 못했어요.\n \n`{error.param}`", color=0xC0FA1B)
			embed.set_author(name="Traceback", icon_url=self.bot.user.avatar_url_as(static_format="png", size=2048))
			embed.set_footer(text=f"Powered by {dev.name}#{dev.discriminator}", icon_url=dev.avatar_url_as(static_format="png", size=2048))
			embed.set_thumbnail(url=ctx.author.avatar_url_as(static_format="png", size=2048))
			await ctx.send(embed=embed)
		else:
			embed = discord.Embed(title="명령어 실행 중 오류 발생", description=f"해당 명령어를 실행하던 도중에 오류가 발생했어요.\n아래 내용을 관리자에게 전달해주세요.\n \n`{error}`", color=0xFF0000)
			embed.set_author(name="Traceback", icon_url=self.bot.user.avatar_url_as(static_format="png", size=2048))
			embed.set_footer(text=f"Powered by {dev.name}#{dev.discriminator}", icon_url=dev.avatar_url_as(static_format="png", size=2048))
			embed.set_thumbnail(url=ctx.author.avatar_url_as(static_format="png", size=2048))
			await ctx.send(embed=embed)

#	@commands.Cog.listener()
#	async def on_message(self, msg):
#		if msg.author.bot:
#			return

#		if msg.channel.type == discord.ChannelType.private:
#			KST = timezone('Asia/Seoul')
#			now = datetime.datetime.utcnow()
#			time = utc.localize(now).astimezone(KST)
#			embed = discord.Embed(title="문의해주셔서 감사해요!", description="문의하신 내용은 아래와 같아요.", color=0xAFFDEF, timestamp=msg.created_at)
#			embed.add_field(name="문의 내용", value=msg.content, inline=False)
#			embed.add_field(name="문의하신 시간", value=time.strftime("%Y년 %m월 %d일 %H시 %M분 %S초"), inline=False)
#			embed.set_author(name="모드메일", icon_url=self.bot.user.avatar_url_as(static_format='png', size=2048))
#			dev = self.bot.get_user(526958314647453706)
#			guild = self.bot.get_guild(702880464893116518)
#			embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format='png', size=2048))
#			embed.set_thumbnail(url=guild.icon_url_as(static_format='png', size=2048))
#			await msg.channel.send(msg.author.mention, embed=embed, delete_after=20)
#			sembed = discord.Embed(title="새 문의가 도착했어요!", description=f"{msg.author.mention} ( {msg.author.id} )", color=0xAFFDEF, timestamp=msg.created_at)
#			sembed.add_field(name="문의 내용", value=msg.content, inline=False)
#			sembed.add_field(name="문의가 들어온 시간", value=time.strftime("%Y년 %m월 %d일 %H시 %M분 %S초"), inline=False)
#			sembed.set_author(name="모드메일", icon_url=self.bot.user.avatar_url_as(static_format='png', size=2048))
#			dev = self.bot.get_user(526958314647453706)
#			guild = self.bot.get_guild(702880464893116518)
#			sembed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format='png', size=2048))
#			sembed.set_thumbnail(url=guild.icon_url_as(static_format='png', size=2048))
#			channel = self.bot.get_channel(712884827912667227)
#			await channel.send("<@&711753639722745896>", embed=sembed)

def setup(bot):
	bot.add_cog(events(bot))
