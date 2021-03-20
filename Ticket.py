# // -- imports to make the bot work on discord -- //
import discord
from discord.ext import commands
import asyncio
# // -- import for database -- //
import sqlite3
# // -- import for random decisions -- //
import random
# // -- import the commonly used methods -- //
import Util

class Ticket(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        conn = sqlite3.connect('Database.db')
        c = conn.cursor()
        c.execute("SELECT channel_ID FROM channel_table WHERE title='TICKET-LOG';")
        self.ticketlog = c.fetchone()
        conn.close()


    @commands.command(name = 'ticket_begins',
                    aliases = ['ticket_begin','tb'])
    @Util.is_admin()
    async def ticket_begins(self, ctx):
        await Util.log_command(self.bot,ctx,"ticket_begins")
        chnl = self.bot.get_channel(Util.HELP_CHNL)
        msg = await chnl.send(embed = discord.Embed(title = "React To This Message To Make A Ticket!",
                description = """ **Welcome to the help desk**
 ___How to use the help desk :__
  - By clicking on the emote below you will be able to create a ticket. A ticket will be a private chatroom between you, the mods, and the CH team. Please do not create a ticket just to talk to the team, as they will not respond, and will stick to chatting in #👥general-public👥 & #👥general-public-2👥 when they plop on.

 Once inside the ticket there are a large assortments of commands that you will have at your disposal. The ones to note are :
 `-rename` newTicketName
 `-invite` @.user

 You should be able to have all the permissions that you need, but if you need any more, feel free to ask a mod in the ticket. The ticket is 100% a safe place where opening one will not get you in any trouble.

 __Some excellent reasons to open a ticket are :__
  - Some one is bullying you
  - Some one is making you feel uncomfortable
  - A Cyanide and Happiness related topic. (Someone stealing their videos, selling their merch 3rd party, or anything along those lines)
  - A personal request that you are not comfortable with sharing in #📍discord-suggestions📍 or in any other chat room.

 Once when a ticket is done, the mods will `-close` the ticket and all of the messages said inside will be logged on Roboberts server. This log is for future reference in the event that someone else is facing a similar problem or if we need to reference previous material.""",
            colour = random.randint(0,0xffffff)))
        await msg.add_reaction("\U0001F4E7")

    @commands.command(name = 'rename')
    @Util.is_chn_in_tick()
    async def rename(self, ctx, *,new_name):
        await Util.log_command(self.bot,ctx,"rename")
        await ctx.channel.edit(name="{} {} {} Ticket".format(ctx.author.name,ctx.author.id,new_name))

    @commands.command(name = 'invite')
    @Util.is_chn_in_tick()
    async def invite(self, ctx, target: discord.Member = None):
        await Util.log_command(self.bot,ctx,"invite")
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages = True
        overwrite.read_messages = True
        overwrite.read_message_history = True
        await ctx.channel.set_permissions(target,overwrite = overwrite)

    @commands.command(name = 'close_ticket',
                    aliases = ['close'])
    @Util.is_admin()
    @Util.is_chn_in_tick()
    async def close_ticket(self, ctx,*, note = ''):
        await Util.log_command(self.bot,ctx,"close_ticket")
        mycontent = ''
        async for msg in ctx.channel.history(limit = 10000):
            mycontent += "\n{} : {} : {}".format(msg.created_at,msg.author,msg.content)
        extension = Util.html_log('tickets',mycontent,ctx.channel.name,ctx.message.id)
        mychn = self.bot.get_channel(int(self.ticketlog[0]))
        embed = discord.Embed(title = "Ticket Closed",
                description = "{} has been closed by {}\nReason : {}\nFor more details visit : https://robobert.tobira.io/tickets/{}".format(
                    ctx.channel.name,
                    ctx.author,
                    note,
                    ("{}{}-{}.txt".format(extension,ctx.channel.name, ctx.message.id))
                    ),
                colour = random.randint(0,0xffffff)
                )
        await mychn.send(embed = embed)
        await ctx.channel.delete()


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if not Util.is_help_desk(payload):
            return
        if payload.user_id == self.bot.user.id:
            return
        await self.bot.http.remove_reaction(payload.channel_id, payload.message_id, payload.emoji, payload.user_id)
        user = await self.bot.get_guild(433695004645523456).fetch_member(payload.user_id)

        for channel in self.bot.get_guild(433695004645523456).channels:
            if str(user.id) in str(channel.name):
                msg = await channel.send(user.mention)
                await msg.delete()
                await channel.send(embed = discord.Embed(title = "{} : You Already Have A Ticket".format(user.name), colour = random.randint(0,0xffffff)))
                return
        channel = await self.bot.get_guild(433695004645523456).create_text_channel(name = "{} {} Ticket".format(user.name,user.id),
                category = self.bot.get_channel(Util.TICKET_CAT)
                )
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages = True
        overwrite.read_messages = True
        overwrite.read_message_history = True
        await channel.set_permissions(user,overwrite = overwrite)
        msg = await channel.send(user.mention)
        await msg.delete()
        await channel.send(embed = discord.Embed(title = "{} Ticket".format(user.name),
            colour = random.randint(0,0xffffff)))

def setup(bot):
    bot.add_cog(Ticket(bot))
