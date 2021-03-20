# // -- imports to make the bot work on discord -- //
import discord
from discord.ext import commands
import asyncio
import random
# // -- imposts to make the captions -- //
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
# // -- import the commonly used methods -- //
import Util

import os

class Caption(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name = 'cc_idiot',
                    aliases = ['ccidiot','idiot'])
    @Util.is_comic_chnl()
    async def cc_idiot(self,ctx):
        await Util.log_command(self.bot,ctx,"cc_idiot")
        def check_message(message):
            return ((message.author == ctx.author) and (message.channel == ctx.channel))
        img = Image.open("../html/images/captions/Idiot.png")
        
        await ctx.send(embed = discord.Embed(title="Please Type Caption",colour = random.randint(0,0xffffff)))
        in_msg = await self.bot.wait_for('message', timeout=120.0, check = check_message)

        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("../html/images/captions/BADABB__.TTF", 42)
        draw.text((12, 480),in_msg.content,(0,0,0),font=font)
        img.save('../html/images/captions/caption.png')      
        embed = discord.Embed(colour = random.randint(0,0xffffff))
        file = discord.File("../html/images/captions/caption.png", filename="caption.png")
        embed.set_image(url="attachment://caption.png")
        await ctx.send(file=file,embed = embed)

    @commands.command(name = 'cc_simple',
                    aliases = ['ccsimple','simple'])
    @Util.is_comic_chnl()
    async def cc_simple(self,ctx):
        await Util.log_command(self.bot,ctx,"cc_simple")
        def check_message(message):
            return ((message.author == ctx.author) and (message.channel == ctx.channel))
        img = Image.open("../html/images/captions/Simple.png")
        
        await ctx.send(embed = discord.Embed(title="Please Type Caption",colour = random.randint(0,0xffffff)))
        in_msg = await self.bot.wait_for('message', timeout=120.0, check = check_message)
        await ctx.send(embed = discord.Embed(title="Please Type The Next Caption",colour = random.randint(0,0xffffff)))
        in_msg2 = await self.bot.wait_for('message', timeout=120.0, check = check_message)

        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("../html/images/captions/BADABB__.TTF", 24)
        draw.text((16, 22),in_msg.content,(0,0,0),font=font)
        draw.text((692, 22),in_msg2.content,(0,0,0),font=font)
        img.save('../html/images/captions/caption.png')      
        embed = discord.Embed(colour = random.randint(0,0xffffff))
        file = discord.File("../html/images/captions/caption.png", filename="caption.png")
        embed.set_image(url="attachment://caption.png")
        await ctx.send(file=file,embed = embed)

    @commands.command(name = 'cc_son',
                    aliases = ['ccson','son'])
    @Util.is_comic_chnl()
    async def cc_son(self,ctx):
        await Util.log_command(self.bot,ctx,"cc_son")
        def check_message(message):
            return ((message.author == ctx.author) and (message.channel == ctx.channel))
        img = Image.open("../html/images/captions/Son.png")
        
        await ctx.send(embed = discord.Embed(title="Please Type Caption",colour = random.randint(0,0xffffff)))
        in_msg = await self.bot.wait_for('message', timeout=120.0, check = check_message)

        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("../html/images/captions/BADABB__.TTF", 42)
        draw.text((40, 440),in_msg.content,(0,0,0),font=font)
        img.save('../html/images/captions/caption.png')      
        embed = discord.Embed(colour = random.randint(0,0xffffff))
        file = discord.File("../html/images/captions/caption.png", filename="caption.png")
        embed.set_image(url="attachment://caption.png")
        await ctx.send(file=file,embed = embed)

    @commands.command(name = 'cc_tattoo',
                    aliases = ['cctattoo','tattoo'])
    @Util.is_comic_chnl()
    async def cc_tattoo(self,ctx):
        await Util.log_command(self.bot,ctx,"cc_tattoo")
        def check_message(message):
            return ((message.author == ctx.author) and (message.channel == ctx.channel))
        img = Image.open("../html/images/captions/Tattoo.png")
        
        await ctx.send(embed = discord.Embed(title="Please Type Caption",colour = random.randint(0,0xffffff)))
        in_msg = await self.bot.wait_for('message', timeout=120.0, check = check_message)

        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("../html/images/captions/BADABB__.TTF", 42)
        draw.text((450, 1030),in_msg.content,(0,0,0),font=font)
        img.save('../html/images/captions/caption.png')      
        embed = discord.Embed(colour = random.randint(0,0xffffff))
        file = discord.File("../html/images/captions/caption.png", filename="caption.png")
        embed.set_image(url="attachment://caption.png")
        await ctx.send(file=file,embed = embed)

    @commands.command(name = 'cc_wisdom',
                    aliases = ['ccwisdom','wisdom'])
    @Util.is_comic_chnl()
    async def cc_wisdom(self,ctx):
        await Util.log_command(self.bot,ctx,"cc_wisdom")
        def check_message(message):
            return ((message.author == ctx.author) and (message.channel == ctx.channel))
        img = Image.open("../html/images/captions/Wisdom.png")
        
        await ctx.send(embed = discord.Embed(title="Please Type Caption",colour = random.randint(0,0xffffff)))
        in_msg = await self.bot.wait_for('message', timeout=120.0, check = check_message)
        await ctx.send(embed = discord.Embed(title="Please Type The Next Caption",colour = random.randint(0,0xffffff)))
        in_msg2 = await self.bot.wait_for('message', timeout=120.0, check = check_message)

        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("../html/images/captions/BADABB__.TTF", 24)
        draw.text((11, 11),in_msg.content,(0,0,0),font=font)
        draw.text((266, 302),in_msg2.content,(0,0,0),font=font)
        img.save('../html/images/captions/caption.png')      
        embed = discord.Embed(colour = random.randint(0,0xffffff))
        file = discord.File("../html/images/captions/caption.png", filename="caption.png")
        embed.set_image(url="attachment://caption.png")
        await ctx.send(file=file,embed = embed)


def setup(bot):
    bot.add_cog(Caption(bot))
