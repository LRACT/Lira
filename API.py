import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=commands.when_mentioned_or("r."), description="Playing with Lucario")
bot.remove_command('help')

modules = [
	'modules.moderation',
	'modules.events',
	'modules.fun',
	'modules.level',
	'modules.default',
	'modules.develop',
	'modules.support',
]

for ext in modules:
	bot.load_extension(ext)

@bot.event
async def on_message(msg):
	if msg.author.bot:
		return
	
	if msg.channel.type == discord.ChannelType.private:
		return

	if msg.content.startswith("r.") or msg.content.startswith(f"<@{bot.user.id}> ") or msg.content.startswith(f"<@!{bot.user.id}> "):
		await bot.process_commands(msg)

bot.run("Token")
