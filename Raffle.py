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

class Raffle(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    def make_total_raffle(self):
        total_raffle = list(Util.RAFFLE)
        for user in Util.DB_RAFFLE:
            total_raffle.append(user[0])
        return total_raffle

    def make_total_points(self,id):
        total_point = dict(Util.POINT)
        for user in Util.DB_POINT:
            if user[0] in total_point:
                total_point[user[0]] += user[1]
            else:
                total_point[user[0]] = user[1]
        if not (id in total_point):
            total_point[id] = 0
        return total_point

    @commands.command(name = 'clear_raffle')
    @Util.is_admin()
    async def clear_raffle(self, ctx,*, content = ''):
        await Util.log_command(self.bot,ctx,"clear_raffle")
        conn = sqlite3.connect('Database.db')
        c = conn.cursor()
        c.execute("DROP TABLE raffle_table;")
        conn.commit()
        sql_cmd = open("SQL_CMDS/c-raffle_table.txt",'r').read()
        c.execute(sql_cmd)
        conn.commit()
        c.execute("SELECT user_ID FROM raffle_table;")
        Util.DB_RAFFLE = c.fetchall()
        conn.close()
        Util.RAFFLE = []
        await ctx.send("The database has been rest")

    @commands.command(name = 'raffle_begins',
                    aliases = ['raffle_begin'])
    @Util.is_admin()
    async def raffle_begins(self, ctx,*, content = ''):
        await Util.log_command(self.bot,ctx,"raffle_begins")
        if content == '':
            ctx.send("{} Please Make Sure To Give A Description Over The Winning Item".format(ctx.author))
            return
        chnl = self.bot.get_channel(Util.RAFFLE_CHNL)
        embed = discord.Embed(title = "React To This Message To Enter Into The Raffle!",
                description = "{}``` ```Each Ticket Entry Costs 3 Points, And You Are Allowed Up To 5 Entries!".format(content),
                colour = random.randint(0,0xffffff)
                )
        embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
        msg = await chnl.send(embed = embed)
        await msg.add_reaction("\U0001F39F")
        await msg.pin()

    @commands.command(name = 'winner')
    @Util.is_admin()
    async def winner(self, ctx,*, content = ''):
        await Util.log_command(self.bot,ctx,"winner")
        total_raffle = self.make_total_raffle()
        chnl = self.bot.get_channel(Util.RAFFLE_CHNL)
        async for message in chnl.history(limit = 10):
            await message.clear_reactions()
        while True:
            try:
                win = total_raffle[random.randint(0,len(total_raffle)-1)]
                member = await ctx.guild.fetch_member(win)
                break
            except:
                continue
        embed = discord.Embed(title = "The Raffle Is Done!",
                    description = "{} is the winner of the raffle!".format(member.mention),
                    colour = random.randint(0,0xffffff))
        await chnl.send(embed = embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if not Util.is_raffle_chnl(payload):
            return
        if payload.user_id == self.bot.user.id:
            return
        await self.bot.http.remove_reaction(payload.channel_id, payload.message_id, payload.emoji, payload.user_id)

        total_raffle = self.make_total_raffle()
        total_point = self.make_total_points(payload.user_id)
        if total_raffle.count(payload.user_id) >= 5:
            return
        if total_point[payload.user_id] < 3:
            return

        if payload.user_id in Util.POINT:
            Util.POINT[payload.user_id] -= 3
        else:
            Util.POINT[payload.user_id] = (-1 * 3)

        chnl = self.bot.get_guild(433695004645523456).get_channel(Util.RAFFLE_CHNL)
        mylist = []
        async for msg in chnl.history(limit = 10):
            mylist.append(msg)
        mylist.pop(-1)
        if len(mylist) > 0:
            await chnl.delete_messages(mylist)
        total_raffle.append(payload.user_id)
        Util.RAFFLE.append(payload.user_id)
        emsg = ''
        overflow = 0
        color = random.randint(0,0xffffff)
        for i in total_raffle:
            try:
                user = await self.bot.get_guild(433695004645523456).fetch_member(i)
            except:
                continue
            emsg += ' ' + user.mention
            overflow += 1
            if overflow == 30:
                embed = discord.Embed(title = 'All The Tickets In The Hat!',
                                description = emsg,
                                colour = color
                                )
                await chnl.send(embed = embed)
                emsg = ''
                overflow = 0
        if emsg != '':
            embed = discord.Embed(title = 'All The Tickets In The Hat!',
                            description = emsg,
                            colour = color
                            )
            await chnl.send(embed = embed)



def setup(bot):
    bot.add_cog(Raffle(bot))
