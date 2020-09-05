import discord
from discord.ext import commands
from pytz import timezone, utc
import datetime
import asyncio
import sqlite3

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
		embed = discord.Embed(title=f"현재 {self.bot.user.name}의 지연 시간", color=0xAFFDEF)
		embed.add_field(name="API Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=False)
		embed.add_field(name="Message Latency", value=f"{round(float(ocha) * 1000)}ms", inline=False)
		embed.add_field(name="Uptime", value=str(uptime).split(".")[0])
		embed.set_thumbnail(url=ctx.author.avatar_url_as(static_format='png', size=2048))
		embed.set_footer(text=f"Powered by {str(owner)}", icon_url=(owner.avatar_url))
		embed.set_author(name="지연 시간", icon_url=self.bot.user.avatar_url)
		await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} - Pong!", embed=embed)

	
	@commands.command()
	@commands.is_owner()
	async def reload(self, ctx, *args):
		self.bot.reload_extension(f"modules.{args[0]}")
		await ctx.send(f":white_check_mark: {ctx.author.mention} - {args[0]} 모듈을 성공적으로 다시 시작했어요.")

	@commands.command()
	@commands.is_owner()
	async def reset(self, ctx):
		humans = self.bot.get_channel(713254695363412070)
		bots = self.bot.get_channel(713254625955807243)
		h = 0
		b = 0
		for m in ctx.guild.members:
			if m.bot:
				b += 1
			else:
				h += 1
		await humans.edit(name=f"멤버 : {h}명")
		await bots.edit(name=f"봇 : {b}개")
		await ctx.send(f"{ctx.author.mention} - 완료!")

	@commands.command()
	@commands.has_role(711753639722745896)
	async def announce(self, ctx, to_announce):
		if ctx.message.content.split(" ")[1] == "everyone":
			queue = ctx.message.content.split(" ")[2:]
			mention = "@everyone"
		elif ctx.message.content.split(" ")[1] == "here":
			queue = ctx.message.content.split(" ")[2:]
			mention = "@here"
		else:
			queue = ctx.message.content.split(" ")[1:]
			mention = None
		announce = ""
		for q in queue:
			announce += f"{q} "
		embed = discord.Embed(title="새로운 커뮤니티 공지사항이에요!", description=f"{announce}\n \n \n*앗, 해결되지 않은 궁금증이나 문의할 내용이 있으신가요? 명령어 채널에서 r.new [ 티켓 내용 ]을 사용해 문의해주세요!*", color=0xFFFCC9, timestamp=ctx.message.created_at)
		embed.set_author(name="전체 공지", icon_url=self.bot.user.avatar_url)
		embed.set_footer(text=f"보낸 이 : {str(ctx.author)}", icon_url=ctx.author.avatar_url)
		embed.set_thumbnail(url=ctx.guild.icon_url)
		msg = await ctx.send(f"{ctx.author.mention} - 아래 내용으로 공지를 전달할거에요. 멘션 대상 : `{mention}`", embed=embed)
		await msg.add_reaction("<:cs_yes:659355468715786262>")
		def check(reaction, user):
			return reaction.message.channel == ctx.channel and user == ctx.author and str(reaction.emoji) == "<:cs_yes:659355468715786262>"
		try:
			reaction, user = await self.bot.wait_for('reaction_add', timeout=60, check=check)
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
		embed = discord.Embed(title=f"{str(self.bot.user)}의 명령어 모음", description=f"**< > 는 필수, [ ] 는 선택형 필드에요.**\n서버에 대한 질문은 명령어 채널에서 r.new [ 티켓 내용 ]을 사용해 문의해주세요!\n봇이 고장난 것 같나요? <@526958314647453706>에게 문의해주세요!", color=0xFFFCC9)
		embed.add_field(name="r.help", value="봇의 도움말을 전송해요.", inline=False)
		embed.add_field(name="r.ping", value="퐁! 봇의 응답 지연 시간을 전송해요.", inline=False)
		embed.add_field(name="r.avatar [ @유저 ]", value="지정한 유저 ( 혹은 본인 )의 아바타( 프로필 사진 )를 불러와요.", inline=False)
		embed.add_field(name="r.infractions < @유저 >", value="지정한 유저의 경고 기록을 불러와요.", inline=False)
		embed.add_field(name="r.rank [ @유저 ]", value="지정한 유저 ( 혹은 본인 )의 경험치 정보를 불러와요.")
		embed.add_field(name="r.new [ 문의 내용 ]", value="지원 티켓 채널을 생성해요.", inline=False)
		embed.add_field(name="r.close", value="지원 티켓 채널을 비활성화해요.", inline=False)
		embed.add_field(name="스타보드", value="서버 내에서 📌 반응이 2개 이상 모이면 <#711809313064222811> 채널에 올라가요.\n*이 기능은 유저의 영구적인 박제 등의 이유로 사용되는 기능이 아니에요. 따라서, 해당 메시지의 주인이 삭제를 원하는 경우에는, 언제든 삭제가 가능해요.*", inline=False)
		role = discord.utils.get(ctx.guild.roles, id=711753639722745896)
		if role in ctx.author.roles:
			embed.add_field(name="r.warn < @유저 > [ 사유 ]", value="유저에게 경고를 부여해요.\n*이 경고는 지우거나 철회하기 힘드니 신중하게 부여하세요!*", inline=False)
			embed.add_field(name="r.mute < @유저 > [ 시간 ] [ 사유 ]", value="유저의 채팅을 제한해요.\n시간을 지정할 경우 타임아웃 후 채팅 제한이 자동으로 해제돼요.", inline=False)
			embed.add_field(name="r.unmute < @유저 > [ 사유 ]", value="유저의 채팅 제한 조치를 해제해요.", inline=False)
			embed.add_field(name="r.kick < @유저 > [ 사유 ]", value="유저를 서버에서 추방해요.\n초대 코드가 있으면 다시 접속할 수 있어요.", inline=False)
			embed.add_field(name="r.ban < @유저 > [ 메시지 지우기 일수 ( ~7일까지 ) ] [ 사유 ]", value="유저를 서버에서 영구적으로 차단해요.\n부계정으로 접속하기 힘들어지고, 초대 코드가 있어도 접속할 수 없어요.", inline=False)
			embed.add_field(name="r.announce [ everyone / here ] < 내용 >", value="<#711738746009288724> 채널에 내용을 전송해요. 멘션을 따로 지정하지 않으면 내용만 전달되어요.", inline=False)
		embed.set_thumbnail(url=ctx.guild.icon_url_as(static_format="png", size=2048))
		embed.set_author(name="도움말", icon_url=self.bot.user.avatar_url)
		dev = self.bot.get_user(526958314647453706)
		embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format="png", size=2048))
		await ctx.send(embed=embed)
		#await ctx.message.add_reaction("✉")
	
	@commands.command()
	@commands.is_owner()
	async def answer(self, ctx, receive: discord.User):
		KST = timezone('Asia/Seoul')
		now = datetime.datetime.utcnow()
		time = utc.localize(now).astimezone(KST)
		queue = ctx.message.content.split(" ")[2:]
		answer_text = ""
		for q in queue:
			answer_text += f"{q} "
		embed = discord.Embed(title="문의에 대해 관리자의 답장이 도착했어요!", description=f"답변한 관리자 : {ctx.author.mention}, ( {ctx.author.id} )", color=0xC0FA1B, timestamp=ctx.message.created_at)
		embed.add_field(name="관리자의 답변 내용", value=answer_text, inline=False)
		embed.add_field(name="답장이 완료된 시각", value=time.strftime("%Y년 %m월 %d일 %H시 %M분 %S초"), inline=False)
		embed.set_author(name="모드메일", icon_url=self.bot.user.avatar_url_as(static_format='png', size=2048))
		dev = self.bot.get_user(526958314647453706)
		embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format='png', size=2048))
		embed.set_thumbnail(url=ctx.guild.icon_url_as(static_format='png', size=2048))
		msg = await ctx.send(f"{ctx.author.mention} - 이 내용으로 {str(receive)} 님에게 전송할 거에요. 내용이 정확한가요?", embed=embed)
		await msg.add_reaction("<:cs_yes:659355468715786262>")
		def check(reaction, user):
			return reaction.message.channel == ctx.channel and user == ctx.author and str(reaction.emoji) == "<:cs_yes:659355468715786262>"
		try:
			reaction, user = await self.bot.wait_for('reaction_add', timeout=60, check=check)
		except asyncio.TimeoutError:
			await msg.clear_reactions()
		else:
			await msg.clear_reactions()
			try:
				await receive.send(receive.mention, embed=embed)
				await msg.edit(content=f"{ctx.author.mention} - 성공적으로 답변을 전송했어요!", embed=None)
			except:
				await msg.edit(content=f"{ctx.author.mention} - 전송에 실패했어요. 해당 유저가 DM을 막아놨거나, 서버에서 나갔어요.", embed=None)
	
	@commands.command(aliases=['profile'])
	async def avatar(self, ctx, users: commands.Greedy[discord.User]):
		if not users:
			user = ctx.author
		else:
			user = users[0]
		dev = self.bot.get_user(526958314647453706)
		embed = discord.Embed(color=0xFFFCC9)
		embed.set_author(name="프로필 사진", icon_url=self.bot.user.avatar_url_as(static_format="png", size=2048))
		embed.set_footer(text=f"Powered by {dev.name}#{dev.discriminator}", icon_url=dev.avatar_url_as(static_format="png", size=2048))
		embed.set_image(url=user.avatar_url_as(static_format="png", size=2048))
		await ctx.send(embed=embed)
		
def setup(bot):
	bot.add_cog(default(bot))
