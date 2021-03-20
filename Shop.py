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

class Shop(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

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

    def remove_points(self,id, amount):
        if id in Util.POINT:
            Util.POINT[id] -= amount
        else:
            Util.POINT[id] = (-1 * amount)

    @commands.command(name = 'buy_color',
                    aliases = ['buy_colour','bcolor','bcolour'])
    @Util.is_shop_chnl()
    async def buy_color(self,ctx, color = "NaN"):
        await Util.log_command(self.bot,ctx,"buy_color")
        total_point = self.make_total_points(ctx.author.id)
        if total_point[ctx.author.id] < 40:
            embed = discord.Embed(title = "Sorry But {}, You Have Insufficient Funds.".format(ctx.author),
                        description = "The Price To Buy A Color Role Is 40 Points. Earn Points By Chatting In The General Chat! Every Message Has A 1/200ish Odds To Give You A Point!",
                        colour = random.randint(0,0xffffff)
                        )
            await ctx.send(embed = embed)
            return
        role_color = ['RED','ORANGE','YELLOW','GREEN','BLUE','PURPLE','WHITE','BLACK','PINK']
        if color.upper() in role_color:
            conn = sqlite3.connect('Database.db')
            c = conn.cursor()
            c.execute("SELECT role_ID FROM role_table WHERE title='{}';".format(color.upper()))
            role = c.fetchone()
            conn.close()
            await ctx.author.add_roles(ctx.guild.get_role(role[0]))
            embed = discord.Embed(title = "{} Transaction Complete!".format(ctx.author),
                        description = "Earn Points By Chatting In The General Chat! Every Message Has A 1/200ish Odds To Give You A Point!",
                        colour = random.randint(0,0xffffff)
                        )
            await ctx.send(embed = embed)
            self.remove_points(ctx.author.id,40)
            return
        embed = discord.Embed(title = "{} Color Not Found!".format(ctx.author),
                    description = "The Possible Colors Are : RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, WHITE, BLACK, PINK",
                    colour = random.randint(0,0xffffff)
                    )
        await ctx.send(embed = embed)

    @commands.command(name = 'change_nickname',
                    aliases = ['change_nick','cn'])
    @Util.is_shop_chnl()
    async def change_nickname(self,ctx,*,nickname = ""):
        await Util.log_command(self.bot,ctx,"change_nickname")
        total_point = self.make_total_points(ctx.author.id)
        if total_point[ctx.author.id] < 1:
            embed = discord.Embed(title = "Sorry But {}, You Have Insufficient Funds.".format(ctx.author),
                        description = "The Price To Change Your Nickname is 1 Point. Earn Points By Chatting In The General Chat! Every Message Has A 1/200ish Odds To Give You A Point!",
                        colour = random.randint(0,0xffffff)
                        )
            await ctx.send(embed = embed)
            return
        await ctx.author.edit(nick = nickname)
        embed = discord.Embed(title = "{} Transaction Complete!".format(ctx.author),
                        description = "Earn Points By Chatting In The General Chat! Every Message Has A 1/200ish Odds To Give You A Point!",
                        colour = random.randint(0,0xffffff)
                        )
        await ctx.send(embed = embed)
        self.remove_points(ctx.author.id,1)

    @commands.command(name = 'make_color',
                    aliases = ['make_coluor','mcolor','mcolour'])
    @Util.is_shop_chnl()
    async def make_color(self,ctx, color_hex = '000000'):
        await Util.log_command(self.bot,ctx,"make_color")
        total_point = self.make_total_points(ctx.author.id)
        if total_point[ctx.author.id] < 250:
            embed = discord.Embed(title = "Sorry But {}, You Have Insufficient Funds.".format(ctx.author),
                        description = "The Price To Buy A Color Role Is 250 Points. Earn Points By Chatting In The General Chat! Every Message Has A 1/100 Odds To Give You A Point!",
                        colour = random.randint(0,0xffffff)
                        )
            await ctx.send(embed = embed)
            return
        if (len(color_hex) != 6) or (color_hex == "000000"):
             await ctx.send("{} is not a 6 digit hex string (000000 too is not accepted, but 000001 is). Ex : ABC123, 00FF00, 123456".format(color_hex))
             return
        hexStr = list(color_hex.lower())
        color = 0
        hexStr.reverse()
        for i in range(len(hexStr)):
            if hexStr[i] == 'a':color += (16**i)*10
            elif hexStr[i] == 'b':color += (16**i)*11
            elif hexStr[i] == 'c':color += (16**i)*12
            elif hexStr[i] == 'd':color += (16**i)*13
            elif hexStr[i] == 'e':color += (16**i)*14
            elif hexStr[i] == 'f':color += (16**i)*15
            else:
                try:
                    color += (16**i)*int(hexStr[i])
                except Exception as error:
                    await ctx.send("{} is not a valid hex number".format(i))
                    return
        roleID = await ctx.guild.create_role(name = str(ctx.author.id), colour = discord.Colour(color))
        await ctx.author.add_roles(roleID)
        embed = discord.Embed(title = "{} Transaction Complete!".format(ctx.author),
                        description = "Earn Points By Chatting In The General Chat! Every Message Has A 1/200ish Odds To Give You A Point!",
                        colour = random.randint(0,0xffffff)
                        )
        await ctx.send(embed = embed)
        self.remove_points(ctx.author.id,250)

    @commands.command(name = 'make_role',
                    aliases = ['mrole'])
    @Util.is_shop_chnl()
    async def make_role(self,ctx, color_hex = '000000',*,role_name = ''):
        await Util.log_command(self.bot,ctx,"make_role")
        total_point = self.make_total_points(ctx.author.id)
        if total_point[ctx.author.id] < 500:
            embed = discord.Embed(title = "Sorry But {}, You Have Insufficient Funds.".format(ctx.author),
                        description = "The Price To Buy A Color Role Is 250 Points. Earn Points By Chatting In The General Chat! Every Message Has A 1/100 Odds To Give You A Point!",
                        colour = random.randint(0,0xffffff)
                        )
            await ctx.send(embed = embed)
            return
        if (len(color_hex) != 6) or (color_hex == "000000"):
             await ctx.send("{} is not a 6 digit hex string (000000 too is not accepted, but 000001 is). Ex : ABC123, 00FF00, 123456".format(color_hex))
             return
        if role_name == '':
            await ctx.send("Please give a name to the role")
            return
        hexStr = list(color_hex.lower())
        color = 0
        hexStr.reverse()
        for i in range(len(hexStr)):
            if hexStr[i] == 'a':color += (16**i)*10
            elif hexStr[i] == 'b':color += (16**i)*11
            elif hexStr[i] == 'c':color += (16**i)*12
            elif hexStr[i] == 'd':color += (16**i)*13
            elif hexStr[i] == 'e':color += (16**i)*14
            elif hexStr[i] == 'f':color += (16**i)*15
            else:
                try:
                    color += (16**i)*int(hexStr[i])
                except Exception as error:
                    await ctx.send("{} is not a valid hex number".format(i))
                    return
        roleID = await ctx.guild.create_role(name = role_name, colour = discord.Colour(color))
        await ctx.author.add_roles(roleID)
        embed = discord.Embed(title = "{} Transaction Complete!".format(ctx.author),
                        description = "Earn Points By Chatting In The General Chat! Every Message Has A 1/200ish Odds To Give You A Point!",
                        colour = random.randint(0,0xffffff)
                        )
        await ctx.send(embed = embed)
        self.remove_points(ctx.author.id,500)

def setup(bot):
    bot.add_cog(Shop(bot))
