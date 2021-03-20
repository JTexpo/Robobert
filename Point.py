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

class Point(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name = 'give_points')
    @Util.is_admin()
    async def give_points(self,ctx, target: discord.Member = None, amount = 0):
        await Util.log_command(self.bot,ctx,"give_points")
        if target == None :
            return
        if target.id in Util.POINT:
            Util.POINT[target.id] += amount
        else:
            Util.POINT[target.id] = amount
        await ctx.send("{} was awarded their {} points.".format(target,amount))


    @commands.command(name = 'all_points',
                        aliases = ['points','point'])
    @Util.is_shop_chnl()
    async def all_points(self,ctx, target: discord.Member = None):
        await Util.log_command(self.bot,ctx,"all_points")
        total_point = dict(Util.POINT)
        for user in Util.DB_POINT:
            if user[0] in total_point:
                total_point[user[0]] += user[1]
            else:
                total_point[user[0]] = user[1]
        if target != None :
            if not (target.id in total_point):
                total_point[target.id] = 0
            embed = discord.Embed(title = "Points on {} : {}".format(target.name, target.id),
                description = "{} has {} points since reset.".format(target.name,total_point[target.id]),
                colour = random.randint(0,0xffffff)
                )
            await ctx.send(embed = embed)
            return

        top_20 = 1
        total_point = sorted(total_point.items(), key = lambda kv: kv[1])
        total_point.reverse()
        embed = discord.Embed(title = "Point Leaderboard",
            description = "Top Point Since Last Reset.",
            colour = random.randint(0,0xffffff)
            )
        for user in total_point:
            try:
                member = await ctx.guild.fetch_member(user[0])
            except:
                continue
            embed.add_field(name = "{} : {}".format(top_20,member.display_name), value = user[1])
            top_20 += 1
            if top_20 == 21:
                break
        await ctx.send(embed = embed)

    
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if not Util.is_point_chnl(ctx):
            return
        member = await ctx.guild.fetch_member(ctx.author.id)
        if random.randint(0,200-len(member.roles)) == 0:
            await ctx.add_reaction(self.bot.get_emoji(679312865441611776))
            if ctx.author.id in Util.POINT:
                Util.POINT[ctx.author.id] += 1
            else:
                Util.POINT[ctx.author.id] = 1

def setup(bot):
    bot.add_cog(Point(bot))
