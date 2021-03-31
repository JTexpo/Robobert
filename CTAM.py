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

class CTAM(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        conn = sqlite3.connect('Database.db')
        c = conn.cursor()
        c.execute("SELECT role_ID FROM role_table WHERE title='NICE';")
        self.nice = c.fetchone()
        c.execute("SELECT role_ID FROM role_table WHERE title='LIT';")
        self.lit = c.fetchone()
        c.execute("SELECT role_ID FROM role_table WHERE title='BEAST';")
        self.beast = c.fetchone()
        c.execute("SELECT role_ID FROM role_table WHERE title='LEET';")
        self.leet = c.fetchone()
        c.execute("SELECT role_ID FROM role_table WHERE title='5878';")
        self.JT = c.fetchone()
        conn.close()
        self.strike = 0
        self.activity = {}

    @commands.command(name = 'countset',
                    aliases = ['count_set','cs'])
    @Util.a_ctam_chnl()
    @Util.is_admin()
    async def countset(self,ctx, number = 0):
        await Util.log_command(self.bot,ctx,"countset")
        Util.COUNT = number+1
        embed = discord.Embed(title = "The Current Number is now {}!".format(Util.COUNT-1),
                description = "This means that the next number you should type is : **{}**".format(Util.COUNT),
                colour = random.randint(0,0xffffff)
                )
        await ctx.send(embed = embed)

    @commands.command(name = 'count')
    @Util.a_ctam_chnl()
    async def count(self,ctx):
        await Util.log_command(self.bot,ctx,"count")
        embed = discord.Embed(title = "The Current Number Is {}!".format(Util.COUNT-1),
                description = "This means that the next number you should type is : **{}**".format(Util.COUNT),
                colour = random.randint(0,0xffffff)
                )
        embed.set_footer(text = "highscore : {}".format(Util.COUNT_HIGH))
        await ctx.send(embed = embed)

    @commands.command(name = 'highscore',
                    aliases = ['high','high_score','hs'])
    @Util.a_ctam_chnl()
    async def highscore(self,ctx):
        await Util.log_command(self.bot,ctx,"highscore")
        embed = discord.Embed(title = "The Current High Score Is : **{}**!".format(Util.COUNT_HIGH),
                colour = random.randint(0,0xffffff)
                )
        await ctx.send(embed = embed)

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if not Util.is_ctam_chnl(ctx):
            return
        try:
            number = int(ctx.content)
        except Exception as error:
            return

        if number == Util.COUNT:
            Util.COUNT = Util.COUNT+1
            #// -- giving roles -- //
            await ctx.add_reaction("\U00002705")
            if number == 69:
                await ctx.author.add_roles(ctx.guild.get_role(self.nice[0]))
            elif number == 420:
                await ctx.author.add_roles(ctx.guild.get_role(self.lit[0]))
            elif number == 666:
                await ctx.author.add_roles(ctx.guild.get_role(self.beast[0]))
            elif number == 1337:
                await ctx.author.add_roles(ctx.guild.get_role(self.leet[0]))
            elif number == 5878:
                await ctx.author.add_roles(ctx.guild.get_role(self.JT[0]))
            if (((number % 100) == 0) and (self.strike > 0)):
                self.strike -= 1
                embed = discord.Embed(title = "Congrats On {}!".format(number),
                    description = "Stikes have been knocked down by 1 as a reward, now at **{}** -> **{}** strikes".format(self.strike+1,self.strike),
                    colour = random.randint(0,0xffffff)
                    )
                mchannel = self.bot.get_channel(Util.CTAM_CHNL[0])
                embed.set_footer(text = "highscore : {}".format(Util.COUNT_HIGH))
                await mchannel.send(embed = embed)
            #// -- updating activity -- //
            if ctx.author.id in self.activity:
                self.activity[ctx.author.id] += 1
            else:
                self.activity[ctx.author.id] = 1

            return
        # since this is a binary statement, returning and proceeding if not returned works. I hate the way that indents work on python which is why I don't want to nest this in an else statement
        # // -- if the count is incorrect -- //
        self.strike += 1
        if self.strike == 3:
            if Util.COUNT > Util.COUNT_HIGH:
                embed = discord.Embed(title = "NEW HIGH SCORE!",
                    description = "{} has been replaced with something even higher! Now lets strive to beat **{}**".format(Util.COUNT_HIGH,Util.COUNT),
                    colour = random.randint(0,0xffffff)
                    )
                Util.COUNT_HIGH = int(Util.COUNT)
                mchannel = self.bot.get_channel(Util.CTAM_CHNL[0])
                embed.set_footer(text = "highscore : {}".format(Util.COUNT_HIGH))
                await mchannel.send(embed = embed)

            embed = discord.Embed(title = "Oh no 3 strikes you're out!",
                description = "**{}** : wrote **{}** which isn't {}.\n\
The current count is set back to 0 \nThis means that the next number you should type is : **1**\nShout out to these members for helping get the count this far!".format(
                ctx.author.mention,ctx.content,Util.COUNT),
                colour = random.randint(0,0xffffff)
                )
            top_20 = 1
            self.activity = sorted(self.activity.items(), key = lambda kv: kv[1])
            self.activity.reverse()
            for user in self.activity:
                embed.add_field(name = "{} : {}".format(top_20,ctx.guild.get_member(user[0])), value = "Counted {} Numbers!".format(user[1]))
                top_20 += 1
                if top_20 == 20:
                    break
            self.activity = {}
            Util.COUNT = 1
            self.strike = 0
        else:
            embed = discord.Embed(title = "Strike {}!".format(self.strike),
                description = "**{}** : wrote **{}** which isn't {}.\n\
The current count is set at {} \nThis means that the next number you should type is : **{}**".format(
                ctx.author.mention,ctx.content,Util.COUNT,Util.COUNT-1,Util.COUNT),
                colour = random.randint(0,0xffffff)
                )
        # // -- displaying the embed -- //
        mchannel = self.bot.get_channel(Util.CTAM_CHNL[0])
        embed.set_footer(text = "highscore : {}".format(Util.COUNT_HIGH))
        await mchannel.send(embed = embed)
        await ctx.add_reaction("\U0000274E")

    @commands.Cog.listener()
    async def on_message_delete(self, ctx):
        if not Util.is_ctam_chnl(ctx):
            return
        try:
            number = int(ctx.content)
        except Exception as error:
            return
        embed = discord.Embed(title = "Watch out everyone we got a troll!",
            description = "**{}** : deleted their number **{}** from the channel.\n\
The current count is {}\nThis means that the next number you should type is : **{}**".format(
            ctx.author.mention,ctx.content,Util.COUNT-1,Util.COUNT),
            colour = random.randint(0,0xffffff)
            )
        embed.set_footer(text = "highscore : {}".format(Util.COUNT_HIGH))
        mchannel = self.bot.get_channel(Util.CTAM_CHNL[0])
        await mchannel.send(embed = embed)
    
    @commands.Cog.listener()
    async def on_message_delete(self, ctx, ctx2):
        if not Util.is_ctam_chnl(ctx):
            return
        try:
            number = int(ctx.content)
        except Exception as error:
            return
        embed = discord.Embed(title = "Watch out everyone we got a troll!",
            description = "**{}** : edited their number **{}** to **{}**.\n\
The current count is {}\nThis means that the next number you should type is : **{}**".format(
            ctx.author.mention,ctx.content,ctx2.content,Util.COUNT-1,Util.COUNT),
            colour = random.randint(0,0xffffff)
            )
        embed.set_footer(text = "highscore : {}".format(Util.COUNT_HIGH))
        mchannel = self.bot.get_channel(Util.CTAM_CHNL[0])
        await mchannel.send(embed = embed)

def setup(bot):
    bot.add_cog(CTAM(bot))
