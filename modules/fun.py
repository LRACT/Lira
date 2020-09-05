import discord
from discord.ext import commands
import sqlite3
import asyncio

class fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if str(payload.emoji) == '📌':
			guild = self.bot.get_guild(payload.guild_id)
			dest = self.bot.get_channel(711809313064222811)
			channel = self.bot.get_channel(payload.channel_id)
			message = await channel.fetch_message(payload.message_id)
			user = payload.member
			role = discord.utils.get(guild.roles, id=711753639722745896)
			if role in user.roles:
				count = 2
			else:
				count = 2
			if message.reactions[0].count >= count:
				conn = sqlite3.connect('discord.sqlite')
				cur = conn.cursor()
				cur.execute(f"SELECT * FROM star WHERE msg = {message.id}")
				rows = cur.fetchall()
				if not rows:
					if message.author.bot != True:
						app = await self.bot.application_info()
						dev = app.owner
						embed = discord.Embed(title="📌을 눌러 박제하기", description=f"[해당 메시지로 이동하기](https://discordapp.com/channels/{guild.id}/{channel.id}/{message.id})", color=0xFFF700)
						embed.add_field(name="채널", value=f"<#{channel.id}>, {channel.id}", inline=False)
						embed.add_field(name="유저", value=f"{str(message.author.mention)}, {message.author.id}", inline=False)
						if message.content == "":
							embed.add_field(name="메시지 내용", value="메시지 내용이 없습니다.", inline=False)
						else:
							embed.add_field(name="메시지 내용", value=message.content, inline=False)
						embed.set_author(name="스타보드", icon_url=self.bot.user.avatar_url_as(static_format='png', size=2048))
						embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url_as(static_format='png', size=2048))	
						if message.attachments:
							att = message.attachments[0]
							if att.filename.endswith('.png') or att.filename.endswith('.jpg') or att.filename.endswith('.gif') or att.filename.endswith('.PNG') or att.filename.endswith('.JPG') or att.filename.endswith('.GIF'):
								aaa = await att.to_file()
								msg = await self.bot.get_channel(711823152002629653).send(file=aaa)
								image = msg.attachments[0].url
								embed.set_image(url=image)
							else:
								embed.add_field(name='파일', value=f'[맨 앞의 파일]({att.url})')
						await dest.send(embed=embed)
						cur.execute(f"INSERT INTO star(msg) VALUES({message.id})")
						conn.commit()
						conn.close()
	@commands.command()
	@commands.is_owner()
	async def call(self, ctx, user: discord.User):
		i = 0
		while i == 0:
			def check(message):
				return message.author == user and message.channel == ctx.channel
			try:
				await self.bot.wait_for('message', timeout=5, check=check)
			except asyncio.TimeoutError:
				await ctx.send(f":telephone_receiver: {user.mention}")
			else:
				i = 1
				await ctx.send(f"{ctx.author.mention} - 호출한 사람 도착!")

def setup(bot):
	bot.add_cog(fun(bot))
