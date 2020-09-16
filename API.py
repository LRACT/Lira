import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=commands.when_mentioned_or("r."), description="리라(이트)")
bot.remove_command('help')

modules = [
	'modules.moderation',
	'modules.events',
	'modules.fun',
	'modules.level',
	'modules.default',
	'modules.develop',
	'modules.support',
	'modules.verify'
]

for ext in modules:
	bot.load_extension(ext)

@bot.event
async def on_message(msg):
	if msg.author.bot:
		return
	
	if msg.channel.type == discord.ChannelType.private:
		return
	
	if msg.guild.id == 702880464893116518:
		manager = msg.guild.get_role(711753639722745896)
		if msg.content.startswith("r.") or msg.content.startswith(f"<@{bot.user.id}> ") or msg.content.startswith(f"<@!{bot.user.id}> "):
			await bot.process_commands(msg)
		elif "discord.gg" in msg.content or "discordapp.com/invite" in msg.content:
			if manager not in msg.author.roles and "[ 초대 승인됨 ]" not in msg.channel.topic:
				await msg.delete()
				await msg.channel.send(f"<:cs_trash:659355468631769101> {msg.author.mention} - Discord 초대 링크 감지, 배너에 초대 링크를 게시해야 하는 경우 관리자에게 문의해주세요.")
		elif "https://" in msg.content or "http://" in msg.content:
			if manager not in msg.author.roles and "[ 링크 승인됨 ]" not in msg.channel.topic:
				await msg.delete()
				await msg.channel.send(f"<:cs_trash:659355468631769101> {msg.author.mention} - 승인되지 않은 링크 업로드 감지, 링크 업로드 관련은 관리자에게 문의해주세요.")
		

bot.run("Token")
