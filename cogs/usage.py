from discord.ext import commands, tasks
from random import randint
import json
import asyncio
import discord
import aiohttp
import random
from discord.ext.commands.cooldowns import BucketType
import time
import math
import pymongo
from pymongo import MongoClient

cluster = MongoClient('mongodb+srv://TenseUp:GosuGosu123@cluster0-ip668.mongodb.net/<dbname>?retryWrites=true&w=majority')
db = cluster["queue"]
guilds = db["guilds"]

class usage(commands.Cog, name="usage"):
    """How to use the bot"""
    def __init__(self,bot, hidden):
        self.bot = bot
        self.hidden = hidden
        self.players = []
        self.channels = []
        self.inqueue = []
        self.owners = ['564798709045526528', '332443859105873920']
        
        
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        embed = discord.Embed(title="Guild Join", description=f'{guild.id}', color=0x00FF00)
        embed.add_field(name=f'{guild.name}', value=f"{len([i for i in guild.members if not i.bot])}")
        support_guild = self.bot.get_guild(725002895459876866)
        support_guild_channel_logs = support_guild.get_channel(727171446983622707)
        with open('queue.json') as f:
          thing = json.load(f)
        thing['main'][str(guild.id)] = {}
        thing['main'][str(guild.id)]['players_one'] = []
        thing['main'][str(guild.id)]['channels'] = []
        thing['main'][str(guild.id)]['queue_one'] = []
        thing['main'][str(guild.id)]['players_two'] = []
        thing['main'][str(guild.id)]['players_three'] = []
        thing['main'][str(guild.id)]['queue_two'] = []
        thing['main'][str(guild.id)]['queue_three'] = []
        with open("queue.json", "w") as f:
              json.dump(thing, f)
        await support_guild_channel_logs.send(embed=embed)
        
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        guilds.delete_one({"_id": str(guild.id)})
        embed = discord.Embed(title="Guild leave", description=f'{guild.id}', color=0xFF0000)
        embed.add_field(name=f'{guild.name}', value=f"{len([i for i in guild.members if not i.bot])}")
        support_guild = self.bot.get_guild(725002895459876866)
        support_guild_channel_logs = support_guild.get_channel(727171446983622707)
        await support_guild_channel_logs.send(embed=embed)
        with open("queue.json") as f:
          thing = json.load(f)
        del thing[str(guild.id)]
        with open("queue.json", "w") as f:
            json.dump(thing, f)

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def newQueue(self,ctx):
        """Making a queue, maxumum of 3"""
        counter = 0
        gi = guilds.find_one({"_id": str(ctx.guild.id)})
        try:
          a = gi['queue_one']
          counter += 1
        except:
          pass
        try:
          a = gi['queue_two']
          counter += 1
        except:
          pass
        try:
          a = gi['queue_three']
          counter += 1
        except:
          pass
        if counter == 3:
          return await ctx.send("Sorry! You can only have 3 queues per server.")
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author
        await ctx.send("Please mention the channel you want as your queue. If you wish to cancel this process, respond with `cancel`.")
        try:
            one_channel = await self.bot.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.author.send("Message timed out")
            return
        if one_channel.content.lower() == 'cancel':
            await ctx.send('Cancelled.')
            return
        else:
            print (one_channel.content)
            one_channel = one_channel.content
            one_channel = one_channel.replace('<#', '')
            one_channel = one_channel.replace('>', '')
            print (one_channel)
        await ctx.send("Please mention the type of queue you would like this to be, for example: `battle`, `2v2`, `match`, etc. If you would like to cancel this action, respond with `cancel`.")
        try:
            type = await self.bot.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.author.send("Message timed out")
            return
        if type.content.lower() == 'cancel':
            await ctx.send('Cancelled.')
            return
        else:
            type = type.content
        await ctx.send("Please mention your Staff role, if you wish to cancel, please respond with `cancel`.")
        try:
            staff = await self.bot.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.author.send("Message timed out")
            return
        if staff.content.lower() == 'cancel':
            await ctx.send("Cancelled.")
        else:
            print (staff.content)
            staff = staff.content
            staff = staff.replace('<@&', '')
            staff = staff.replace('>', '')
            print (staff)
            already = guilds.find_one({"_id": str(ctx.guild.id)})
            if not already:
              channel = ctx.guild.get_channel(int(one_channel))
              embed = discord.Embed(title=f"Queue here for: {type}!", description='React with the ✋ below to queue!')
              msg = await channel.send(embed=embed)
              await msg.add_reaction("✋")
              guilds.insert_one({"_id": str(ctx.guild.id), "queue_one": int(one_channel), "type_one": str(type), "staff_one": int(staff), "msg_one": int(msg.id)})
              await channel.send("@everyone", delete_after=0)
              await ctx.send('Bot successfully set up.')
            else:
              channel = ctx.guild.get_channel(int(one_channel))
              embed = discord.Embed(title=f"Queue here for: {type}!", description='React with the ✋ below to queue!', color=0x0000FF)
              msg = await channel.send(embed=embed)
              await msg.add_reaction("✋")
              try:
                checker = already['queue_one']
              except:
                checker = None
              if not checker:
                guilds.update_one({"_id": str(ctx.guild.id)}, {"$set": {"queue_one":int(one_channel), "type_one": str(type), "staff_one": int(staff), "msg_one": int(msg.id)}})
              else:
                try:
                  checker_two = already['queue_two']
                except:
                  checker_two = None
                if not checker_two:
                  guilds.update_one({"_id": str(ctx.guild.id)}, {"$set": {"queue_two":int(one_channel), "type_two": str(type), "staff_two": int(staff), "msg_two": int(msg.id)}})
                else:
                  guilds.update_one({"_id": str(ctx.guild.id)}, {"$set": {"queue_three":int(one_channel), "type_three": str(type), "staff_three": int(staff), "msg_three": int(msg.id)}})
              await channel.send("@everyone", delete_after=0)
              await ctx.send('Bot successfully set up.')
              
    @commands.command(hidden=True)
    async def aaa(self,ctx):
        a = False
        for x in self.owners:
          if str(ctx.author.id) == x:
            a = True
        if a == False:
          return await ctx.send('Sorry! this command is owner exclusive, and contains private data.')
        with open('queue.json') as f:
          jsona = json.load(f)
        await ctx.send(jsona)
            
    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        gi = guilds.find_one({"_id": str(payload.guild_id)})
        guild = self.bot.get_guild(payload.guild_id)
        try:
          first = gi['msg_one']
        except:
          first = 'PlaceHolder'
        try:
          second = gi['msg_two']
        except:
          second = 'PlaceHolder'
        try:
          third = gi['msg_three']
        except:
          third = 'PlaceHolder'
        one = False
        two = False
        three = False
        print(first)
        print(str(payload.message_id))
        if str(payload.message_id) == str(first):
          print("ok")
          one = True
        elif str(payload.message_id) == str(second):
          two = True
        elif str(payload.message_id) == str(third):
          three = True
        if one == True:
          print("one")
          cha = gi['queue_one']
          channel = guild.get_channel(int(cha))
          ms = gi["msg_one"]
          type = gi["type_one"]
          msg = await channel.fetch_message(ms)
          reactions = [z.emoji for z in msg.reactions]
          if str(payload.emoji) in reactions:
            user = payload.member
            if user.bot:
              return
            with open('queue.json') as f:
                  queue = json.load(f)
            await msg.remove_reaction(payload.emoji, user)
            if queue['main'][str(guild.id)]['players_one'] == []:
              # {guildID : {"players" : [userId, userID], "channels": [channelID, channelID], "queue" : [userId, userId]}}
              
                  
                  
              # self.players.append(f"{str(user.id)}")
              nangle = discord.Embed(title='⌛ Finding a match...', description='Please stand by. If you wish to unqueue, use the command `q!unqueue` here.', color=0x0000FF)
              bingle = await user.send(embed=nangle)
              # self.inqueue.append(f"{str(user.id)}")
              # self.inqueue.append(f"{str(bingle.id)}")
              queue['main'][str(guild.id)]['players_one'].append(str(user.id))
              queue['main'][str(guild.id)]['queue_one'].append(str(user.id)) #becuase it is a list ok
              queue['main'][str(guild.id)]['queue_one'].append(str(bingle.id)) #yeah?
              with open('queue.json', 'w') as f:
                  json.dump(queue, f)
            else:
              queue['main'][str(guild.id)]['players_one'].append(str(user.id))
              # self.players.append(f"{str(user.id)}")
              nangle = discord.Embed(title='⌛ Finding a match...', description='Please stand by. If you wish to unqueue, use the command `q!unqueue` here.', color=0x0000FF)
              dingle = await user.send(embed=nangle)
              # player1 = await self.bot.fetch_user(int(self.players[0]))
              # player2 = await self.bot.fetch_user(int(self.players[1]))
              playerOne = guild.get_member(int(queue['main'][str(guild.id)]['players_one'][0])) #how about this? then you get member object not user yeah better
              playerTwo = guild.get_member(int(queue['main'][str(guild.id)]['players_one'][1]))
              wongle = discord.Embed(title='✅ Match found! Check the discord server!', description='The channel will be located on top of all the text channels.', color=0x00FF00)
              await dingle.edit(embed=wongle)
              if queue['main'][str(guild.id)]['queue_one']:
                useren = guild.get_member(int(queue['main'][str(guild.id)]['queue_one'][0]))
                gingle = await useren.fetch_message(int(queue['main'][str(guild.id)]['queue_one'][1]))
                queue['main'][str(guild.id)]['queue_one'].clear()
                wongle = discord.Embed(title='✅ Match found! Check the discord server!', description='The channel will be located on top of all the text channels.', color=0x00FF00)
                await gingle.edit(embed=wongle)
                pass
              else:
                pass
              queue['main'][str(guild.id)]['players_one'].clear()
              everyone = guild.default_role
              staffe = gi["staff_one"]
              staff = guild.get_role(staffe)
              overwrites = {
                  playerOne: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                  playerTwo: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                  everyone: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                  staff: discord.PermissionOverwrite(read_messages=True, send_messages=True)
              }
              channel = await guild.create_text_channel(f'{playerOne.name} vs {playerTwo.name}', overwrites=overwrites)
              channelembed = discord.Embed(title=f'**{type}**', description='*Welcome two players! Discuss IGNs and whatnot.*', color=0x00FF00)
              channelembed.add_field(name='**__Match Details__**', value=f'\nPlayer1: {playerOne.mention}\nPlayer2: {playerTwo.mention}', inline=False)
              channelembed.add_field(name='Need to contact staff? Type `q!support` and staff will be with you shortly!', value='Don\'t excessivley spam this command!', inline=False)
              channelembed.add_field(name='Need to backout? Type `q!close`!',value="Don't dodge though!", inline=False)
              channelembed.add_field(name='Need to add a friend?', value='Use `q!adduser <user mention>` to add them.', inline=False)
              channelembed.add_field(name='Need to remove a friend? Removing the rival will result in a warning.', value='Use `q!removeuser <user mention>` to remove them.', inline=False)
              print(channel.id)
              self.channels.append(f"{channel.id}")
              print(self.channels)
              await channel.send(embed=channelembed)
              await channel.send(f"{playerOne.mention}{playerTwo.mention}")
              with open('queue.json', 'w') as f:
                  json.dump(queue, f)
        elif two == True:
          cha = gi['queue_two']
          channel = guild.get_channel(int(cha))
          ms = gi["msg_two"]
          type = gi["type_two"]
          msg = await channel.fetch_message(ms)
          reactions = [z.emoji for z in msg.reactions]
          if str(payload.emoji) in reactions:
            user = payload.member
            if user.bot:
              return
            with open('queue.json') as f:
                  queue = json.load(f)
            await msg.remove_reaction(payload.emoji, user)
            if queue['main'][str(guild.id)]['players_two'] == []:
              # {guildID : {"players" : [userId, userID], "channels": [channelID, channelID], "queue" : [userId, userId]}}
              
                  
                  
              # self.players.append(f"{str(user.id)}")
              nangle = discord.Embed(title='⌛ Finding a match...', description='Please stand by. If you wish to unqueue, use the command `q!unqueue` here.', color=0x0000FF)
              bingle = await user.send(embed=nangle)
              # self.inqueue.append(f"{str(user.id)}")
              # self.inqueue.append(f"{str(bingle.id)}")
              queue['main'][str(guild.id)]['players_two'].append(str(user.id))
              queue['main'][str(guild.id)]['queue_two'].append(str(user.id)) #becuase it is a list ok
              queue['main'][str(guild.id)]['queue_two'].append(str(bingle.id)) #yeah?
              with open('queue.json', 'w') as f:
                  json.dump(queue, f)
            else:
              queue['main'][str(guild.id)]['players_two'].append(str(user.id))
              # self.players.append(f"{str(user.id)}")
              nangle = discord.Embed(title='⌛ Finding a match...', description='Please stand by. If you wish to unqueue, use the command `q!unqueue` here.', color=0x0000FF)
              dingle = await user.send(embed=nangle)
              # player1 = await self.bot.fetch_user(int(self.players[0]))
              # player2 = await self.bot.fetch_user(int(self.players[1]))
              playerOne = guild.get_member(int(queue['main'][str(guild.id)]['players_two'][0])) #how about this? then you get member object not user yeah better
              playerTwo = guild.get_member(int(queue['main'][str(guild.id)]['players_two'][1]))
              wongle = discord.Embed(title='✅ Match found! Check the discord server!', description='The channel will be located on top of all the text channels.', color=0x00FF00)
              await dingle.edit(embed=wongle)
              if queue['main'][str(guild.id)]['queue_two']:
                useren = guild.get_member(int(queue['main'][str(guild.id)]['queue_two'][0]))
                gingle = await useren.fetch_message(int(queue['main'][str(guild.id)]['queue_two'][1]))
                queue['main'][str(guild.id)]['queue_two'].clear()
                wongle = discord.Embed(title='✅ Match found! Check the discord server!', description='The channel will be located on top of all the text channels.', color=0x00FF00)
                await gingle.edit(embed=wongle)
                pass
              else:
                pass
              queue['main'][str(guild.id)]['players_two'].clear()
              everyone = guild.default_role
              staffe = gi["staff_two"]
              staff = guild.get_role(staffe)
              overwrites = {
                  playerOne: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                  playerTwo: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                  everyone: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                  staff: discord.PermissionOverwrite(read_messages=True, send_messages=True)
              }
              channel = await guild.create_text_channel(f'{playerOne.name} vs {playerTwo.name}', overwrites=overwrites)
              channelembed = discord.Embed(title=f'**{type}**', description='*Welcome two players! Discuss IGNs and whatnot.*', color=0x00FF00)
              channelembed.add_field(name='**__Match Details__**', value=f'\nPlayer1: {playerOne.mention}\nPlayer2: {playerTwo.mention}', inline=False)
              channelembed.add_field(name='Need to contact staff? Type `q!support` and staff will be with you shortly!', value='Don\'t excessivley spam this command!', inline=False)
              channelembed.add_field(name='Need to backout? Type `q!close`!',value="Don't dodge though!", inline=False)
              channelembed.add_field(name='Need to add a friend?', value='Use `q!adduser <user mention>` to add them.', inline=False)
              channelembed.add_field(name='Need to remove a friend? Removing the rival will result in a warning.', value='Use `q!removeuser <user mention>` to remove them.', inline=False)
              print(channel.id)
              self.channels.append(f"{channel.id}")
              print(self.channels)
              await channel.send(embed=channelembed)
              await channel.send(f"{playerOne.mention}{playerTwo.mention}")
              with open('queue.json', 'w') as f:
                  json.dump(queue, f)

        elif three == True:
          cha = gi['queue_three']
          channel = guild.get_channel(int(cha))
          ms = gi["msg_three"]
          type = gi["type_three"]
          msg = await channel.fetch_message(ms)
          reactions = [z.emoji for z in msg.reactions]
          if str(payload.emoji) in reactions:
            user = payload.member
            if user.bot:
              return
            with open('queue.json') as f:
                  queue = json.load(f)
            await msg.remove_reaction(payload.emoji, user)
            if queue['main'][str(guild.id)]['players_three'] == []:
              # {guildID : {"players" : [userId, userID], "channels": [channelID, channelID], "queue" : [userId, userId]}}
              
                  
                  
              # self.players.append(f"{str(user.id)}")
              nangle = discord.Embed(title='⌛ Finding a match...', description='Please stand by. If you wish to unqueue, use the command `q!unqueue` here.', color=0x0000FF)
              bingle = await user.send(embed=nangle)
              # self.inqueue.append(f"{str(user.id)}")
              # self.inqueue.append(f"{str(bingle.id)}")
              queue['main'][str(guild.id)]['players_three'].append(str(user.id))
              queue['main'][str(guild.id)]['queue_three'].append(str(user.id)) #becuase it is a list ok
              queue['main'][str(guild.id)]['queue_three'].append(str(bingle.id)) #yeah?
              with open('queue.json', 'w') as f:
                  json.dump(queue, f)
            else:
              queue['main'][str(guild.id)]['players_three'].append(str(user.id))
              # self.players.append(f"{str(user.id)}")
              nangle = discord.Embed(title='⌛ Finding a match...', description='Please stand by. If you wish to unqueue, use the command `q!unqueue` here.', color=0x0000FF)
              dingle = await user.send(embed=nangle)
              # player1 = await self.bot.fetch_user(int(self.players[0]))
              # player2 = await self.bot.fetch_user(int(self.players[1]))
              playerOne = guild.get_member(int(queue['main'][str(guild.id)]['players_three'][0])) #how about this? then you get member object not user yeah better
              playerTwo = guild.get_member(int(queue['main'][str(guild.id)]['players_three'][1]))
              wongle = discord.Embed(title='✅ Match found! Check the discord server!', description='The channel will be located on top of all the text channels.', color=0x00FF00)
              await dingle.edit(embed=wongle)
              if queue['main'][str(guild.id)]['queue_three']:
                useren = guild.get_member(int(queue['main'][str(guild.id)]['queue_three'][0]))
                gingle = await useren.fetch_message(int(queue['main'][str(guild.id)]['queue_three'][1]))
                queue['main'][str(guild.id)]['queue_three'].clear()
                wongle = discord.Embed(title='✅ Match found! Check the discord server!', description='The channel will be located on top of all the text channels.', color=0x00FF00)
                await gingle.edit(embed=wongle)
                pass
              else:
                pass
              queue['main'][str(guild.id)]['players_three'].clear()
              everyone = guild.default_role
              staffe = gi["staff_three"]
              staff = guild.get_role(staffe)
              overwrites = {
                  playerOne: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                  playerTwo: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                  everyone: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                  staff: discord.PermissionOverwrite(read_messages=True, send_messages=True)
              }
              channel = await guild.create_text_channel(f'{playerOne.name} vs {playerTwo.name}', overwrites=overwrites)
              channelembed = discord.Embed(title=f'**{type}**', description='*Welcome two players! Discuss IGNs and whatnot.*', color=0x00FF00)
              channelembed.add_field(name='**__Match Details__**', value=f'\nPlayer1: {playerOne.mention}\nPlayer2: {playerTwo.mention}', inline=False)
              channelembed.add_field(name='Need to contact staff? Type `q!support` and staff will be with you shortly!', value='Don\'t excessivley spam this command!', inline=False)
              channelembed.add_field(name='Need to backout? Type `q!close`!',value="Don't dodge though!", inline=False)
              channelembed.add_field(name='Need to add a friend?', value='Use `q!adduser <user mention>` to add them.', inline=False)
              channelembed.add_field(name='Need to remove a friend? Removing the rival will result in a warning.', value='Use `q!removeuser <user mention>` to remove them.', inline=False)
              print(channel.id)
              self.channels.append(f"{channel.id}")
              print(self.channels)
              await channel.send(embed=channelembed)
              await channel.send(f"{playerOne.mention}{playerTwo.mention}")
              with open('queue.json', 'w') as f:
                  json.dump(queue, f)
                                
    @commands.command()
    async def close(self,ctx):
        for x in self.channels:
          if str(ctx.channel.id) == x:
            await ctx.channel.delete()
            return
        await ctx.send("You can't close this channel!")

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def edit(self,ctx):
        def check(m):
          return m.channel == ctx.channel and m.author == ctx.author
        await ctx.send("Which queue would you like to edit? Use, queue_one, queue_two, or queue_three to edit them.")
        try:
            which = await self.bot.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.author.send("Message timed out")
            return
        which = which.content
        gi = guilds.find_one({"_id": str(ctx.guild.id)})
        one = False
        two = False
        three = False
        if which == 'queue_one':
          one = True
        elif which == 'queue_two':
          two = True
        elif which == 'queue_three':
          three = True
        else:
          return await ctx.send("Invalid choice.")
        if one == True:
          def check(m):
              return m.channel == ctx.channel and m.author == ctx.author
          await ctx.send("Please mention the channel you want as your queue. If you wish to cancel this process, respond with `cancel`.")
          try:
              one_channel = await self.bot.wait_for('message', timeout=60.0, check=check)
          except asyncio.TimeoutError:
              await ctx.author.send("Message timed out")
              return
          if one_channel.content.lower() == 'cancel':
              await ctx.send('Cancelled.')
              return
          else:
              print (one_channel.content)
              one_channel = one_channel.content
              one_channel = one_channel.replace('<#', '')
              one_channel = one_channel.replace('>', '')
              print (one_channel)
          await ctx.send("Please mention the type of queue you would like this to be, for example: `battle`, `2v2`, `match`, etc. If you would like to cancel this action, respond with `cancel`.")
          try:
              type = await self.bot.wait_for('message', timeout=60.0, check=check)
          except asyncio.TimeoutError:
              await ctx.author.send("Message timed out")
              return
          if type.content.lower() == 'cancel':
              await ctx.send('Cancelled.')
              return
          else:
              type = type.content
          await ctx.send("Please mention your Staff role, if you wish to cancel, please respond with `cancel`.")
          try:
              staff = await self.bot.wait_for('message', timeout=60.0, check=check)
          except asyncio.TimeoutError:
              await ctx.author.send("Message timed out")
              return
          if staff.content.lower() == 'cancel':
              await ctx.send("Cancelled.")
          else:
              print (staff.content)
              staff = staff.content
              staff = staff.replace('<@&', '')
              staff = staff.replace('>', '')
              print (staff)
              channel = ctx.guild.get_channel(int(one_channel))
              embed = discord.Embed(title=f"Queue here for: {type}!", description='React with the ✋ below to queue!', color=0x0000FF)
              msg = await channel.send(embed=embed)
              await msg.add_reaction("✋")
              guilds.update_one({"_id": str(ctx.guild.id)}, {"$set": {"queue_one":int(one_channel), "type_one": str(type), "staff_one": int(staff), "msg_one": int(msg.id)}})
              await channel.send("@everyone", delete_after=0)
              await ctx.send('Bot successfully set up.')
              return
        elif two == True:
          def check(m):
              return m.channel == ctx.channel and m.author == ctx.author
          await ctx.send("Please mention the channel you want as your queue. If you wish to cancel this process, respond with `cancel`.")
          try:
              one_channel = await self.bot.wait_for('message', timeout=60.0, check=check)
          except asyncio.TimeoutError:
              await ctx.author.send("Message timed out")
              return
          if one_channel.content.lower() == 'cancel':
              await ctx.send('Cancelled.')
              return
          else:
              print (one_channel.content)
              one_channel = one_channel.content
              one_channel = one_channel.replace('<#', '')
              one_channel = one_channel.replace('>', '')
              print (one_channel)
          await ctx.send("Please mention the type of queue you would like this to be, for example: `battle`, `2v2`, `match`, etc. If you would like to cancel this action, respond with `cancel`.")
          try:
              type = await self.bot.wait_for('message', timeout=60.0, check=check)
          except asyncio.TimeoutError:
              await ctx.author.send("Message timed out")
              return
          if type.content.lower() == 'cancel':
              await ctx.send('Cancelled.')
              return
          else:
              type = type.content
          await ctx.send("Please mention your Staff role, if you wish to cancel, please respond with `cancel`.")
          try:
              staff = await self.bot.wait_for('message', timeout=60.0, check=check)
          except asyncio.TimeoutError:
              await ctx.author.send("Message timed out")
              return
          if staff.content.lower() == 'cancel':
              await ctx.send("Cancelled.")
          else:
              print (staff.content)
              staff = staff.content
              staff = staff.replace('<@&', '')
              staff = staff.replace('>', '')
              print (staff)
              channel = ctx.guild.get_channel(int(one_channel))
              embed = discord.Embed(title=f"Queue here for: {type}!", description='React with the ✋ below to queue!', color=0x0000FF)
              msg = await channel.send(embed=embed)
              await msg.add_reaction("✋")
              guilds.update_one({"_id": str(ctx.guild.id)}, {"$set": {"queue_two":int(one_channel), "type_two": str(type), "staff_two": int(staff), "msg_two": int(msg.id)}})
              await channel.send("@everyone", delete_after=0)
              await ctx.send('Bot successfully set up.')
              return
        elif three == True:
          def check(m):
              return m.channel == ctx.channel and m.author == ctx.author
          await ctx.send("Please mention the channel you want as your queue. If you wish to cancel this process, respond with `cancel`.")
          try:
              one_channel = await self.bot.wait_for('message', timeout=60.0, check=check)
          except asyncio.TimeoutError:
              await ctx.author.send("Message timed out")
              return
          if one_channel.content.lower() == 'cancel':
              await ctx.send('Cancelled.')
              return
          else:
              print (one_channel.content)
              one_channel = one_channel.content
              one_channel = one_channel.replace('<#', '')
              one_channel = one_channel.replace('>', '')
              print (one_channel)
          await ctx.send("Please mention the type of queue you would like this to be, for example: `battle`, `2v2`, `match`, etc. If you would like to cancel this action, respond with `cancel`.")
          try:
              type = await self.bot.wait_for('message', timeout=60.0, check=check)
          except asyncio.TimeoutError:
              await ctx.author.send("Message timed out")
              return
          if type.content.lower() == 'cancel':
              await ctx.send('Cancelled.')
              return
          else:
              type = type.content
          await ctx.send("Please mention your Staff role, if you wish to cancel, please respond with `cancel`.")
          try:
              staff = await self.bot.wait_for('message', timeout=60.0, check=check)
          except asyncio.TimeoutError:
              await ctx.author.send("Message timed out")
              return
          if staff.content.lower() == 'cancel':
              await ctx.send("Cancelled.")
          else:
              print (staff.content)
              staff = staff.content
              staff = staff.replace('<@&', '')
              staff = staff.replace('>', '')
              print (staff)
              channel = ctx.guild.get_channel(int(one_channel))
              embed = discord.Embed(title=f"Queue here for: {type}!", description='React with the ✋ below to queue!', color=0x0000FF)
              msg = await channel.send(embed=embed)
              await msg.add_reaction("✋")
              guilds.update_one({"_id": str(ctx.guild.id)}, {"$set": {"queue_three":int(one_channel), "type_three": str(type), "staff_three": int(staff), "msg_three": int(msg.id)}})
              await channel.send("@everyone", delete_after=0)
              await ctx.send('Bot successfully set up.')
              return
                                
                                
    @commands.command()
    async def unqueue(self,ctx):
        with open('queue.json') as f:
          queue = json.load(f)
        for x in queue['main']:
          for z in queue['main'][str(x)]['queue_one']:
            if z == str(ctx.author.id):
                guild = self.bot.get_guild(int(x))
        if queue['main'][str(guild.id)]['queue_one']:
          user = queue['main'][str(guild.id)]['queue_one'][0]
          message = queue['main'][str(guild.id)]['queue_one'][1]
          if ctx.author.id == int(user):
            usere = await self.bot.fetch_user(int(user))
            msg = await usere.fetch_message(message)
            gi = guilds.find_one({"_id": str(guild.id)})
            type = gi['type_one']
            cancelembed = discord.Embed(title="❌Cancelled!", description=f'Queue again if you wish to find another {type}.', color=0xFF0000)
            queue['main'][str(guild.id)]['queue_one'].clear()
            queue['main'][str(guild.id)]['players_one'].clear()
            await msg.edit(embed=cancelembed)
            await ctx.send("Queue cancelled.")
            with open('queue.json', 'w') as f:
                json.dump(queue, f)
          else:
            await ctx.send("You can't do this!")
        else:
          await ctx.send("You can't do this!")
        for x in queue['main']:
          for z in queue['main'][str(x)]['queue_two']:
            if z == str(ctx.author.id):
                guild = self.bot.get_guild(int(x))
        if queue['main'][str(guild.id)]['queue_two']:
          user = queue['main'][str(guild.id)]['queue_two'][0]
          message = queue['main'][str(guild.id)]['queue_two'][1]
          if ctx.author.id == int(user):
            usere = await self.bot.fetch_user(int(user))
            msg = await usere.fetch_message(message)
            gi = guilds.find_one({"_id": str(guild.id)})
            type = gi['type_two']
            cancelembed = discord.Embed(title="❌Cancelled!", description=f'Queue again if you wish to find another {type}.', color=0xFF0000)
            queue['main'][str(guild.id)]['queue_two'].clear()
            queue['main'][str(guild.id)]['players_two'].clear()
            await msg.edit(embed=cancelembed)
            await ctx.send("Queue cancelled.")
            with open('queue.json', 'w') as f:
                json.dump(queue, f)
          else:
            await ctx.send("You can't do this!")
        else:
          await ctx.send("You can't do this!")
        for x in queue['main']:
          for z in queue['main'][str(x)]['queue_three']:
            if z == str(ctx.author.id):
                guild = self.bot.get_guild(int(x))
        if queue['main'][str(guild.id)]['queue_three']:
          user = queue['main'][str(guild.id)]['queue_three'][0]
          message = queue['main'][str(guild.id)]['queue_three'][1]
          if ctx.author.id == int(user):
            usere = await self.bot.fetch_user(int(user))
            msg = await usere.fetch_message(message)
            gi = guilds.find_one({"_id": str(guild.id)})
            type = gi['type_three']
            cancelembed = discord.Embed(title="❌Cancelled!", description=f'Queue again if you wish to find another {type}.', color=0xFF0000)
            queue['main'][str(guild.id)]['queue_three'].clear()
            queue['main'][str(guild.id)]['players_three'].clear()
            await msg.edit(embed=cancelembed)
            await ctx.send("Queue cancelled.")
            with open('queue.json', 'w') as f:
                json.dump(queue, f)
          else:
            await ctx.send("You can't do this!")
        else:
          await ctx.send("You can't do this!")
                                
    
    @commands.command()
    async def support(self,ctx):
        gi = guilds.find_one({"_id": str(ctx.guild.id)})
        staf = gi["staff_one"]
        staff = ctx.guild.get_role(int(staf))
        await ctx.send(f"{staff.mention}", delete_after=0)
        staffe = discord.Embed(title='Staff is on their way!', description='Please be patient', color=0x0000FF)
        await ctx.send(embed=staffe)
        return
      
    @commands.command()
    async def adduser(self, ctx, user:discord.Member):
        """Add a user to your ticket"""
        mandingo = False
        for x in self.channels:
          if str(ctx.channel.id) == str(x):
            mandingo = True
        if mandingo == False:
          await ctx.send("You can't use this here!")
          return
        await ctx.channel.set_permissions(user, read_messages=True, send_messages=True)
        await ctx.send(f"{ctx.author.mention} added {user.mention} to this ticket ( {ctx.channel.mention} ) ")
        
    @commands.command()
    async def removeuser(self, ctx, user:discord.Member):
        """Remove a user from your ticket"""
        mandingo = False
        for x in self.channels:
          if str(ctx.channel.id) == str(x):
           mandingo = True
        if mandingo == False:
          await ctx.send("You can't use this here!")
          return
        await ctx.channel.set_permissions(user, read_messages=False, send_messages=False)
        await ctx.send(f"{ctx.author.mention} removed {user.mention} from this ticket ( {ctx.channel.mention} ) ")
          
                                
                                
def setup(bot):
    bot.add_cog(usage(bot, False))