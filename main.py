import discord 
from discord.ext import commands
from discord.utils import get
from helpers.colour import color
import traceback
import difflib
import sys
from datetime import datetime
import time
import asyncio
import os
import pymongo
from pymongo import MongoClient

cluster = MongoClient('mongodb+srv://TenseUp:GosuGosu123@cluster0-ip668.mongodb.net/<dbname>?retryWrites=true&w=majority')
db = cluster["queue"]
guilds = db["guilds"]


def fmtTime():
	_time = datetime.now()
	return _time.strftime("%b %d %Y %H:%M:%S")


#region colours
blue = color.BLUE
endc = color.END
bold = color.BOLD
purple = color.PURPLE
green = color.GREEN
red = color.RED
yellow = color.YELLOW
#endregion

def printProgressBar(iteration, total, prefix= '', suffix = '', decimals = 1, length = 100, fill = "█", printEnd = "\r"):
	percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
	filledLength = int(length * iteration // total)
	bar = fill * filledLength + '-' * (length - filledLength)
	if iteration == total: 
		print(f'\r{purple}Loading Complete:             |{bar}| {percent}% {suffix}{endc}', end = printEnd)
	elif iteration in [0, 1]:
		print(f'\r{purple}{prefix} |{bar}| {percent}%   {suffix}{endc}', end = printEnd)
	else:
		print(f'\r{purple}{prefix} |{bar}| {percent}%  {suffix}{endc}', end = printEnd)




bot = commands.Bot(command_prefix="q!")


cogs = ['cogs.util', 'cogs.usage']


@bot.event
async def on_command_error(ctx, exception):
	if type(exception) == commands.CommandOnCooldown:
		await ctx.send("{} is on cooldown for {:0.2f} seconds.".format(ctx.command, exception.retry_after), delete_after=5)
	elif type(exception) == commands.CommandNotFound:
		cmd = ctx.message.content.split()[0][1:]
		try:
			closest = difflib.get_close_matches(cmd.lower(), list(bot.all_commands))[0]
		except IndexError:
			await ctx.send("{} is not a known command.".format(cmd), delete_after=5)
		else:
			await ctx.send("{} is not a command, did you mean {}?".format(cmd, closest), delete_after=5)
	elif type(exception) == commands.CheckFailure:
		await ctx.send("You failed to meet a requirement for that ""command.", delete_after=5)
	elif type(exception) == commands.MissingRequiredArgument:
		await ctx.send("You are missing a required argument for that ""command.", delete_after=5)
	elif type(exception) == commands.BadArgument:
		await ctx.send("Invalid Argument.", delete_after=5)
	elif type(exception) == commands.MissingRole:
		await ctx.send("You don't have the required roles to perform that.", delete_after=5)
	elif type(exception) == commands.MissingPermissions:
		await ctx.send("You don't have the required permissions to perform that.", delete_after=5)
	else:
		print(exception)
	print('Ignoring exception in command {}'.format(ctx.command),
		  file=sys.stderr)
	traceback.print_exception(type(exception), exception, exception.__traceback__, file=sys.stderr) 


@bot.event
async def on_ready():
    bot.remove_command("help")
    print(f"{yellow}Loading the beast: {bot.user.name}!{endc}\n")
    time.sleep(1)
    l = len(cogs)
    printProgressBar(0, l, prefix = f'\nInitializing:                ', suffix = 'Complete', length = 50)
    for i, cog in enumerate(cogs):
        time.sleep(0.3)
        printProgressBar(i + 1, l, prefix = f'Loading:{" " * (20 - len(cog))} {cog}', suffix = 'Complete', length = 50)
        bot.load_extension(cog)
    print(f"{yellow}\nInitializing Bot, Please wait...{endc}\n")
    time.sleep(2)
    print(f'{green}Cogs loaded... Bot is now ready and waiting for prefix "."{endc}')

    print(f'{green}\n√ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √  {endc}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="q!help"))
    return



@bot.command(name='reload',
			 description='Reloads bot',
			 aliases=['-r'],
			 hidden=True,
			 case_insensitive=True)
async def reload(ctx):
	# await ctx.channel.purge(limit=int(1))
	""" Reloads cogs while bot is still online """
	owners = ['564798709045526528', '332443859105873920']
	a = False
	for x in owners:
		if x == str(ctx.author.id):
			a = True
	if a == False:
		return await ctx.send("Sorry, this command is owner exclusive.")
	user = ctx.author
	roles = ctx.message.author.roles
	server_id = ctx.guild.id
	updated_cogs = ''
	#clearterm()
	l = len(cogs)
	#await add_command(ctx.guild.id)
	printProgressBar(0, l, prefix = '\nInitializing:', suffix = 'Complete', length = 50)
	for i, cog in enumerate(cogs):
		printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
		bot.unload_extension(cog)
		#print("Reloading", cog)
		bot.load_extension(cog)
		updated_cogs += f'{cog}\n'
	print((f"\nInitializing Bot, Please wait...\n", "purple"))
	print((f'Cogs loaded... Bot is now ready and waiting for prefix "."', "green"))
	await ctx.send(f"`Cogs reloaded by:` <@{user.id}>")
      
@bot.command(hidden=True)
async def getInvite(ctx, guildId:int, guildChannel:int):
    """This command is owner only, it can't be used by non-owners"""
    guild_guild = bot.get_guild(guildId)
    guild_channel = guild_guild.get_channel(guildChannel)
    if ctx.author.id == 564798709045526528: 
      guild_guild = bot.get_guild(guildId)
      guild_channel = guild_guild.get_channel(guildChannel)
      link = await guild_channel.create_invite(max_age='300', unique=False)
      await ctx.author.send(link)
      await ctx.send('check ur dms')
    elif ctx.author.id == 332443859105873920:
      guild_guild = bot.get_guild(guildId)
      guild_channel = guild_guild.get_channel(guildChannel)
      link = await guild_channel.create_invite(max_age='300', unique=False)
      await ctx.author.send(link)
      await ctx.send('check ur dms')
    else:
      await ctx.send("Sorry, but this command is exclusive to the owners, and you are non-owner.")

discord_key = os.getenv("BOT_TOKEN")
# keep_alive.keep_alive()
bot.run('NzI1MDA0NDk1MjAwODQ1ODM1.XvoByg.7hYVbsDrhBEQ3s2t9Ux0GRkuimg', bot=True, reconnect=True)