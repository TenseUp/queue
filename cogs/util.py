from discord.ext import commands
from random import randint
import json
import asyncio
import discord
import aiohttp
import random
from discord.ext.commands.cooldowns import BucketType
import time
import math
from pymongo import MongoClient

class util(commands.Cog):
    """Utilities"""
    def __init__(self, bot, hidden):
        self.hidden = hidden
        self.bot = bot
        
    @commands.command()
    async def help(self, ctx, *cog):
        """Displays the help command
        Anything in angled brackets <> is a required argument. Square brackets [] mark an optional argument"""
        if not ctx.guild:
            prefix = "q!"
        else:
            prefix = "q!"
            # guild = guilds.find_one({"_id": ctx.guild.id})
            # prefix = guild["prefix"]
        if not cog:
            embed = discord.Embed(title="Help", description=f"use `{prefix}help [category|command]` for more info", color=0x00FF00)
            embed.set_footer(text=f"Created by Tense#7987")
            cog_desc = ''
            for x in self.bot.cogs:
                if not self.bot.cogs[x].hidden:
                    cmd = ''
                    cog_desc += f"__**{x}**__: {self.bot.cogs[x].__doc__}\n"
                    for y in self.bot.get_cog(x).get_commands():
                        cmd += f"`{prefix}{y}`,  "
                    embed.add_field(name=f"__**{x}**__: {self.bot.cogs[x].__doc__}", value=cmd, inline=False)
            embed.add_field(name="Links:", value="[Invite the bot](https://discord.com/api/oauth2/authorize?client_id=725004495200845835&permissions=8&scope=bot) | [Bot Shop Server](https://discord.gg/FgcSSbV) | [Support Server](https://discord.gg/2P8v9cU)", inline=False)
            await ctx.send(embed=embed)
        else:
            if len(cog) > 1:
                await ctx.send("That is not a valid category")
            else:
                found = False
                for x in self.bot.cogs:
                    for y in cog:
                        if x == y:
                            #title="Help", description=f"**Category {cog[0]}:** {self.bot.cogs[cog[0]].__doc__}", 
                            embed = discord.Embed(title="Help", color=0x00FF00)
                            scog_info = ''
                            for c in self.bot.get_cog(y).get_commands():
                                if not c.hidden:
                                    scog_info += f"\n**`{c.name}`**: {c.help}\n"
                            embed.add_field(name=f"\n{cog[0]} Category:\n{self.bot.cogs[cog[0]].__doc__}\n ", value=f"\n{scog_info}\n", inline=False)
                            found = True

            if not found:
                for x in self.bot.cogs:
                    for c in self.bot.get_cog(x).get_commands():
                        if c.name == cog[0]:
                            embed = discord.Embed(color=0x00FF00)
                            embed.add_field(name=f"{c.name}: {c.help}", value=f"Usage:\n `{prefix}{c.qualified_name} {c.signature}`")
                            found = True
            if not found:
                embed = discord.Embed(description="Command not found. Check that you have spelt it correctly and used capitals where appropriate")
            await ctx.send(embed=embed)
            
    @commands.command()
    async def invite(self,ctx):
        embed = discord.Embed(title=None, description='[Click here to invite me to any server!](https://discord.com/api/oauth2/authorize?client_id=725004495200845835&permissions=8&scope=bot)', color=0x0000FF)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(util(bot, False))