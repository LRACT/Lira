import discord
from discord.ext import commands
import ast
import asyncio
import sqlite3
import os
import random

def insert_returns(body):
	if isinstance(body[-1], ast.Expr):
		body[-1] = ast.Return(body[-1].value)
		ast.fix_missing_locations(body[-1])

	if isinstance(body[-1], ast.If):
		insert_returns(body[-1].body)
		insert_returns(body[-1].orelse)

	if isinstance(body[-1], ast.With):
		insert_returns(body[-1].body)

class develop(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(aliases=['pre'])
	@commands.is_owner()
	async def presence(self, ctx, *args):
		conn = sqlite3.connect('discord.sqlite')
		cur = conn.cursor()
		cur.execute("SELECT * FROM bot")
		rows = cur.fetchall()
		if args[0] == "온라인":
			st = "온라인 / Online"
			status = discord.Status.online
			local = args[1:]
		elif args[0] == "자리비움":
			st = "자리비움 / Idle"
			status = discord.Status.idle
			local = args[1:]
		elif args[0] == "다른" and args[1] == "용무" and args[2] == "중":
			st = "다른 용무 중 / Do not disturb"
			status = discord.Status.dnd
			local = args[3:]
		elif args[0] == "오프라인":
			st = "오프라인 / Offline"
			status = discord.Status.offline
			local = args[1:]
		else:
			await ctx.send(f'{ctx.author.mention} - 그런 상태 없다.')
			return
		text = ""
		for arg in local:
			text += f"{arg} "
		msg = await ctx.send(f"{ctx.author.mention} - 봇의 상태를 이렇게 변경할거에요. 이게 맞나요?\n상태 : {rows[0][2]} -> {st}\n메시지 : {rows[0][3]} -> {text}")
		await msg.add_reaction("<:cs_yes:659355468715786262>")
		def check(reaction, user):
			return reaction.message.channel == ctx.channel and user == ctx.author and str(reaction.emoji) == "<:cs_yes:659355468715786262>"
		try:
			reaction, user = await self.bot.wait_for('reaction_add', timeout=30, check=check)
		except asyncio.TimeoutError:
			await msg.clear_reactions()
		else:
			await msg.clear_reactions()
			await self.bot.change_presence(status=status, activity=discord.Game(text))
			cur.execute(f"""UPDATE bot SET status = "{st}", activity = "{text}" """)
			conn.commit()
			conn.close()
			await msg.edit(content=f"{ctx.author.mention} - 완료되었어요!")

	@commands.command(aliases=['evaluate', 'execute'])
	@commands.is_owner()
	async def eval(self, ctx, *, command):	
		fn_name = "_eval_expr"
		command = command.strip("` ")
		command = "\n".join(f"    {i}" for i in command.splitlines())
		body = f"async def {fn_name}():\n{command}"
		parsed = ast.parse(body)
		body = parsed.body[0].body
		insert_returns(body)

		env = {
			'bot': ctx.bot,
			'discord': discord,
			'commands': commands,
			'ctx': ctx,
			'__import__': __import__,
			'sqlite3': sqlite3,
			'asyncio': asyncio,
			'os': os,
			'random': random
		}
		exec(compile(parsed, filename="<ast>", mode="exec"), env)

		result = (await eval(f"{fn_name}()", env))
		if result is not None:
			await ctx.send(f":busstop: {ctx.author.mention} - 성공적으로 실행됨:\n```{result}```")
		else:
			await ctx.send(f":busstop: {ctx.author.mention} - 성공적으로 실행됨: `결과 없음.`")
	
	@commands.command(aliases=['directory'])
	async def dir(self, ctx, *args):
		if args:
			path = ""
			if len(args) != 1:
				for arg in args:
					if arg != args[len(args) - 1]:
						path += f"{arg} "
					else:
						path += arg
			else:
                                path += args[0]
			files = os.listdir(path)
			flist = ""
			for file in files:
				flist += f"{file}\n"
			embed = discord.Embed(title=f"{path} 경로의 파일 목록", description=f"```\n{flist}```", color=0xC0FFEE)
			embed.set_author(name="디렉토리", icon_url=self.bot.user.avatar_url)
			dev = self.bot.get_user(526958314647453706)
			embed.set_footer(text=f"Powered by {str(dev)}", icon_url=dev.avatar_url)
			embed.set_thumbnail(url=ctx.author.avatar_url_as(static_format="png", size=2048))
			await ctx.send(ctx.author.mention, embed=embed)

def setup(bot):
	bot.add_cog(develop(bot))
