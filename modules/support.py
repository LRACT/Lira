import discord
from discord.ext import commands
import sqlite3
import asyncio

class support(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def new(self, ctx, *args):
		conn = sqlite3.connect("discord.sqlite")
		cur = conn.cursor()
		cur.execute("SELECT * FROM bot")
		rows = cur.fetchall()
		temp = rows[0][1]
		if len(str(temp)) == 1:
			number = f"000{temp}"
		elif len(str(temp)) == 2:
			number = f"00{temp}"
		elif len(str(temp)) == 3:
			number = f"0{temp}"
		else:
			number = temp

		category = self.bot.get_channel(715125391290925107)
		staffs = ctx.guild.get_role(711753639722745896)
		overwrites = {
			ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True, manage_channels=True, manage_roles=True, read_message_history=True),
			staffs: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True, manage_channels=True, manage_roles=True, read_message_history=True),
			ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True),
			ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False)
		}
		channel = await ctx.guild.create_text_channel(name=f"지원_{number}", topic=f"{str(ctx.author)} ( {ctx.author.id} ) 님의 티켓이에요.", overwrites=overwrites, category=category, reason=f"{str(ctx.author)}님의 티켓 개설 요청")
		if not args:
			desc = "직접 물어보세요!"
		else:
			desc = ""
			for arg in args:
				desc += f"{arg} "
		embed = discord.Embed(title=f"{str(ctx.author)}님이 지원 티켓을 만드셨어요.", description=f"지원 요청한 주요 내용 : {desc}\n \n*잠시만 기다려주세요. 지원 팀이 최대한 빨리 티켓을 확인하고 답장할 거에요!*", color=0xFFFCC9)
		embed.set_author(name="지원", icon_url=self.bot.user.avatar_url)
		dev = self.bot.get_user(526958314647453706)
		embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url)
		embed.set_thumbnail(url=ctx.guild.icon_url_as(static_format="png", size=2048))		
		msg = await channel.send("@here", embed=embed)
		await msg.pin()
		cur.execute(f"UPDATE bot SET tickno = {int(temp) + 1}")
		conn.commit()
		conn.close()
		await ctx.message.add_reaction("<:cs_yes:659355468715786262>")
	
	@commands.command()
	async def close(self, ctx):
		if ctx.channel.category.id != 715125391290925107:
			await ctx.send(f"{ctx.author.mention} - 이 명령어는 지원 티켓 채널에서만 사용하실 수 있어요!")
		else:
			staffs = ctx.guild.get_role(711753639722745896)
			if str(ctx.author.id) in ctx.channel.topic or staffs in ctx.author.roles:
				msg = await ctx.send(f"{ctx.author.mention} - 정말로 이 티켓 채널을 비활성화하실 건가요? 비활성화 된 후에는 복구할 수 없어요!\n<:cs_yes:659355468715786262> - 예\n<:cs_no:659355468816187405> - 아니오")
				await msg.add_reaction("<:cs_yes:659355468715786262>")
				await msg.add_reaction("<:cs_no:659355468816187405>")
				def check(reaction, user):
					return reaction.message.id == msg.id and user == ctx.author
				try:
					reaction, user = await self.bot.wait_for('reaction_add', timeout=60, check=check)
				except asyncio.TimeoutError:
					await msg.clear_reactions()
				else:
					await msg.clear_reactions()
					if str(reaction.emoji) == "<:cs_yes:659355468715786262>":
						await msg.edit(content=f"{ctx.author.mention} - 알겠어요! 5초 후에 채널이 자동으로 비활성화될 거에요.")
						await asyncio.sleep(5)
						a = ctx.channel.topic.split("(")[1]
						ida = a.split(")")[0]
						user = ctx.guild.get_member(int(ida))
						if user is not None:
							await ctx.channel.set_permissions(user, overwrite=None, reason="티켓 채널 닫기")
						deprecated = self.bot.get_channel(715156102857228288)
						await ctx.channel.edit(category=deprecated)
						await user.send(f"{ctx.author.mention} - <#{ctx.channel.id}> 채널이 닫혔어요. 티켓을 다시 여시려면 아래 채널 ID를 사용해 `r.open [ ID ]` 명령어를 사용해주세요.\n채널 ID : {ctx.channel.id}")
					else:
						await msg.edit(content=f"{ctx.author.mention} - 알겠어요! 티켓 채널 비활성화를 취소했어요.")
			else:
				await ctx.send(f"{ctx.author.mention} - 이 채널은 당신이 연 티켓 채널이 아니에요! 당신은 이 티켓 채널을 닫으실 수 없어요.")
	
	@commands.command()
	async def open(self, ctx, channel: discord.TextChannel):
		if channel.category.id != 715156102857228288:
			await ctx.send(f"{ctx.author.mention} - 이 명령어는 닫힌 지원 티켓 채널에 대해서만 사용하실 수 있어요!")
		else:
			staffs = ctx.guild.get_role(711753639722745896)
			if str(ctx.author.id) in channel.topic or staffs in ctx.author.roles:
				msg = await ctx.send(f"{ctx.author.mention} - 티켓 채널을 정말로 다시 여시겠어요?\n<:cs_yes:659355468715786262> - 예\n<:cs_no:659355468816187405> - 아니오")
				await msg.add_reaction("<:cs_yes:659355468715786262>")
				await msg.add_reaction("<:cs_no:659355468816187405>")
				def check(reaction, user):
					return reaction.message.id == msg.id and user == ctx.author
				try:
					reaction, user = await self.bot.wait_for('reaction_add', timeout=60, check=check)
				except asyncio.TimeoutError:
					await msg.clear_reactions()
				else:
					await msg.clear_reactions()
					if str(reaction.emoji) == "<:cs_yes:659355468715786262>":
						await msg.edit(content=f"{ctx.author.mention} - 티켓 채널을 다시 열었어요.")
						a = channel.topic.split("(")[1]
						ida = a.split(")")[0]
						user = ctx.guild.get_member(int(ida))
						overwrites = {
							ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True, manage_channels=True, manage_roles=True, read_message_history=True),
							staffs: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True, manage_channels=True, manage_roles=True, read_message_history=True),
							user: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True, manage_channels=True, manage_roles=True),
							ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False)
						}
						await channel.edit(overwrite=overwrites, reason="티켓 채널 다시 열림")
						activated = self.bot.get_channel(715125391290925107)
						await channel.edit(category=activated)
						embed = discord.Embed(title=f"{str(ctx.author)}님이 지원 티켓을 다시 여셨어요.", description=f"*잠시만 기다려주세요. 지원 팀이 최대한 빨리 티켓을 확인하고 답장할 거에요!*", color=0xFFFCC9)
						embed.set_author(name="지원", icon_url=self.bot.user.avatar_url)
						dev = self.bot.get_user(526958314647453706)
						embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url)
						embed.set_thumbnail(url=ctx.guild.icon_url_as(static_format="png", size=2048))
						await channel.send(f"@here", embed=embed)
					else:
						await msg.edit(content=f"{ctx.author.mention} - 티켓 채널 다시 열기가 취소되었어요.")
			else:
				await ctx.send(f"{ctx.author.mention} - 이 채널은 당신이 연 티켓 채널이 아니에요! 당신은 이 티켓 채널을 다시 열 수 없어요.")

def setup(bot):
	bot.add_cog(support(bot))