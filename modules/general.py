import discord
from discord.ext import commands
from pytz import timezone, utc
import datetime
import asyncio
import sqlite3
import typing

class default(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command()
	async def ping(self, ctx):
		channel = self.bot.get_channel(663806206376149073)
		first_time = datetime.datetime.now()
		m = await channel.send("핑1")
		await m.edit(content="핑2")
		last_time = datetime.datetime.now()
		await m.delete()
		ocha = str(last_time - first_time)[6:]
		owner = self.bot.get_user(526958314647453706)
		conn = sqlite3.connect('discord.sqlite')
		cur = conn.cursor()
		cur.execute('SELECT * FROM bot')
		rows = cur.fetchall()
		record = str(rows[0][0].split(".")[0])
		start_time = datetime.datetime.strptime(record, '%Y-%m-%d %H:%M:%S')
		uptime = (datetime.datetime.now() - start_time)
		embed = discord.Embed(title=f"현재 리라(이트)의 지연 시간", color=0xAFFDEF)
		embed.add_field(name="API Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=False)
		embed.add_field(name="Message Latency", value=f"{round(float(ocha) * 1000)}ms", inline=False)
		embed.add_field(name="Uptime", value=str(uptime).split(".")[0])
		embed.set_thumbnail(url=ctx.author.avatar_url_as(static_format='png', size=2048))
		embed.set_footer(text=f"Powered by {str(owner)}", icon_url=(owner.avatar_url))
		embed.set_author(name="지연 시간", icon_url=self.bot.user.avatar_url)
		await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} - Pong!", embed=embed)

	@commands.command()
	@commands.has_role(711753639722745896)
	async def announce(self, ctx, mention: typing.Optional[str], *, announcement):
		if mention == "everyone":
			mention = "@everyone"
		elif mention == "here":
			mention = "@here"
		else:
			mention = None
		embed = discord.Embed(title="새로운 커뮤니티 공지사항이에요!", description=f"{announcement}\n \n \n*앗, 해결되지 않은 궁금증이나 문의할 내용이 있으신가요? 명령어 채널에서 r.new [ 티켓 내용 ]을 사용해 문의해주세요!*", color=0xFFFCC9, timestamp=ctx.message.created_at)
		embed.set_author(name="전체 공지", icon_url=self.bot.user.avatar_url)
		embed.set_footer(text=f"보낸 이 : {str(ctx.author)}", icon_url=ctx.author.avatar_url)
		embed.set_thumbnail(url=ctx.guild.icon_url)
		msg = await ctx.send(f"{ctx.author.mention} - 아래 내용으로 공지를 전달할거에요. 멘션 대상 : `{mention}`", embed=embed)
		await msg.add_reaction("<:cs_yes:659355468715786262>")
		def check(reaction, user):
			return reaction.message.id == msg.id and user == ctx.author and str(reaction.emoji) == "<:cs_yes:659355468715786262>"
		try:
			await self.bot.wait_for('reaction_add', timeout=60, check=check)
		except asyncio.TimeoutError:
			await msg.clear_reactions()
		else:
			await msg.clear_reactions()
			channel = self.bot.get_channel(711738746009288724)
			if mention != None:
				await channel.send(mention, embed=embed)
				await msg.edit(content=f"{ctx.author.mention} - <#711738746009288724> 채널에 전송 완료했어요!", embed=None)
			else:
				await channel.send(embed=embed)
				await msg.edit(content=f"{ctx.author.mention} - <#711738746009288724> 채널에 전송 완료했어요!", embed=None)

	@commands.command(aliases=['commands'])
	async def help(self, ctx):
		embed = discord.Embed(title=f"리라(이트)의 명령어 모음", description=f"**< > 는 필수, [ ] 는 선택형 필드에요.**\n서버 및 봇에 대한 문의는 티켓을 열어 문의해주세요!", color=0xFFFCC9)
		embed.add_field(name="r.help", value="봇의 도움말을 전송해요.", inline=False)
		embed.add_field(name="r.ping", value="퐁! 봇의 응답 지연 시간을 전송해요.", inline=False)
		embed.add_field(name="r.avatar [ @유저 ]", value="지정한 유저 ( 혹은 본인 )의 아바타( 프로필 사진 )를 불러와요.", inline=False)
		embed.add_field(name="r.infractions < @유저 >", value="지정한 유저의 경고 기록을 불러와요.", inline=False)
		embed.add_field(name="r.rank [ @유저 ]", value="지정한 유저 ( 혹은 본인 )의 경험치 정보를 불러와요.")
		embed.add_field(name="r.new [ 문의 내용 ]", value="지원 티켓 채널을 생성해요.", inline=False)
		embed.add_field(name="r.open < 채널 ID >", value="비활성화된 지원 티켓 채널을 다시 열어요.", inline=False)
		embed.add_field(name="r.close", value="지원 티켓 채널을 비활성화해요.", inline=False)
		role = discord.utils.get(ctx.guild.roles, id=711753639722745896)
		if role in ctx.author.roles:
			embed.add_field(name="r.announce [ everyone / here ] < 내용 >", value="<#711738746009288724> 채널에 내용을 전송해요. 멘션을 따로 지정하지 않으면 내용만 전달되어요.", inline=False)
			embed.add_field(name="r.purge < 1 - 100 사이의 정수 >", value="명령어를 실행한 채팅 채널의 메시지를 삭제해요.", inline=False)
			embed.add_field(name="r.warn < @유저 > [ 사유 ]", value="유저에게 경고를 부여해요.\n*이 경고는 지우거나 철회하기 힘드니 신중하게 부여하세요!*", inline=False)
			embed.add_field(name="r.mute < @유저 > [ 시간 ] [ 사유 ]", value="유저의 채팅을 제한해요.\n시간을 지정할 경우 타임아웃 후 채팅 제한이 자동으로 해제돼요.", inline=False)
			embed.add_field(name="r.unmute < @유저 > [ 사유 ]", value="유저의 채팅 제한 조치를 해제해요.", inline=False)
			embed.add_field(name="r.kick < @유저 > [ 사유 ]", value="유저를 서버에서 추방해요.\n초대 코드가 있으면 다시 접속할 수 있어요.", inline=False)
			embed.add_field(name="r.ban < @유저 > [ 메시지 지우기 일수 ( ~7일까지 ) ] [ 사유 ]", value="유저를 서버에서 영구적으로 차단해요.\n부계정으로 접속하기 힘들어지고, 초대 코드가 있어도 접속할 수 없어요.", inline=False)
		embed.add_field(name="스타보드", value="서버 내에서 📌 반응이 2개 이상 모이면 <#711809313064222811> 채널에 올라가요.\n*이 기능은 유저의 영구적인 박제 등의 이유로 사용되는 기능이 아니에요. 따라서, 해당 메시지의 주인이 삭제를 원하는 경우에는, 언제든 삭제가 가능해요.*", inline=False)
		embed.set_thumbnail(url=ctx.guild.icon_url_as(static_format="png", size=2048))
		embed.set_author(name="명령어 목록", icon_url=self.bot.user.avatar_url)
		dev = self.bot.get_user(526958314647453706)
		embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format="png", size=2048))
		try:
			await ctx.author.send(embed=embed)
		except:
			await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - 개인 메시지가 승인되지 않아 전송에 실패했어요.\n서버의 개인정보 보호 설정에서 `서버 멤버가 보내는 개인 메시지 허용하기.`를 켜주세요.")
		else:
			await ctx.message.add_reaction("✉")
	
	@commands.command(aliases=['profile'])
	async def avatar(self, ctx, user: typing.Optional[discord.User] = None):
		if user is None:
			user = ctx.author
		dev = self.bot.get_user(526958314647453706)
		embed = discord.Embed(color=0xFFFCC9)
		embed.set_author(name=f"{user}님의 프로필 사진", icon_url=self.bot.user.avatar_url_as(static_format="png", size=2048))
		embed.set_footer(text=f"Powered by {dev}", icon_url=dev.avatar_url_as(static_format="png", size=2048))
		embed.set_image(url=user.avatar_url_as(static_format="png", size=2048))
		await ctx.send(embed=embed)
		
def setup(bot):
	bot.add_cog(default(bot))
