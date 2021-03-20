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

class Activity(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name = 'activity')
    async def activity(self,ctx, target: discord.Member = None):
        await Util.log_command(self.bot,ctx,"activity")
        total_activity = dict(Util.ACTIVITY)
        for user in Util.DB_ACTIVITY:
            if user[0] in total_activity:
                total_activity[user[0]] += user[1]
            else:
                total_activity[user[0]] = user[1]
        if target != None :
            if not (target.id in total_activity):
                total_activity[target.id] = 0
            embed = discord.Embed(title = "Activity on {} : {}".format(target.name, target.id),
                description = "{} has sent {} since reset.".format(target.name,total_activity[target.id]),
                colour = random.randint(0,0xffffff)
                )
            await ctx.send(embed = embed)
            return

        top_20 = 1
        total_activity = sorted(total_activity.items(), key = lambda kv: kv[1])
        total_activity.reverse()
        embed = discord.Embed(title = "Activity Leaderboard",
            description = "Top Active Since Last Reset.",
            colour = random.randint(0,0xffffff)
            )
        for user in total_activity:
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
        if ctx.author.id in Util.ACTIVITY:
            Util.ACTIVITY[ctx.author.id] += 1
        else:
            Util.ACTIVITY[ctx.author.id] = 1

def setup(bot):
    bot.add_cog(Activity(bot))
