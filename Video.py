# // -- imports to make the bot work on discord -- //
import discord
from discord.ext import commands
import asyncio
# // -- import for database -- //
import random
# // -- import for script crawling -- //
import urllib.request as urllib2
# // -- import the commonly used methods -- //
import Util

class Video(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    # // -- Main Comic Command -- //
    @commands.command(name = 'video')
    @Util.is_comic_chnl()
    async def video(self,ctx):
        # // -- There are two different types of comics, this will help pick which comic is picked -- //
        v = random.randint(0,2)
        if v == 2:
            await self.randomvideo.invoke(ctx)
        elif v == 1:
            await self.randompodcast.invoke(ctx)
        else:
            await self.randommini.invoke(ctx)


    @commands.command(name = "randommini",
                        aliases = ["mini"])
    @Util.is_comic_chnl()
    async def randommini(self,ctx):
        attempt = 0
        # // -- Creating the base embed -- //
        embd = discord.Embed(title = "A Random Mini",
                          description = ("[Click Here To View Another](http://explosm.net/minis/random)"),
                          colour = random.randint(0,0xffffff))
        embd.set_image(url = "http://explosm.net/img/logo.png")
        while True:
            await Util.log_command(self.bot,ctx,"randommini : 0".format(attempt))
            try:
                link  = ('http://explosm.net/minis/random')
            except Exception as error:
                await Util.error_log_command(self.bot,ctx,"randommini",error)
                return

            pageSource = str(urllib2.urlopen(link).read()).split()
            for i in pageSource:
                if 'youtube.com/watch' in i:
                    p = i[i.index('"')+1:-1]
                    await ctx.send(embed = embd)
                    await ctx.send(p)
                    return


    @commands.command(name = "randompodcast",
                        aliases = ["podcast","rp"])
    @Util.is_comic_chnl()
    async def randompodcast(self,ctx):
        attempt = 0
        embd = discord.Embed(title = "A Random Podcast",
                          description = ("[Click Here To View Most Recent](http://explosm.net/podcasts)"),
                          colour = random.randint(0,0xffffff))
        embd.set_image(url = 'http://files.explosm.net/podcasts/podcast_show_5ad66d6f3e91d_here-s-an-idea_splash.png')
        embd.set_thumbnail(url = "http://explosm.net/img/logo.png")
        while True:
            await Util.log_command(self.bot,ctx,"randompodcast : {}".format(attempt))
            try:
                link  = ('http://explosm.net/podcasts/random')
            except Exception as error:
                await Util.error_log_command(self.bot,ctx,"randompodcast",error)
                return
            pageSource = str(urllib2.urlopen(link).read()).split()
            for i in pageSource:
                if 'href="http://explosm.net/podcasts/' in i:
                    p = i[i.index('"')+1:-1]
                    await ctx.send(embed = embd)
                    await ctx.send(p)
                    return


    @commands.command(name = "randomvideo",
                        aliases = ["rv"])
    @Util.is_comic_chnl()
    async def randomvideo(self,ctx):
        attempt = 0
        embd = discord.Embed(title = "A Random Video",
                          description = ("[Click Here To View Another](http://explosm.net/shorts/random)"),
                          colour = random.randint(0,0xffffff))
        embd.set_image(url = "http://explosm.net/img/logo.png")
        while True:
            await Util.log_command(self.bot,ctx,"randomvideo : {}".format(attempt))
            try:
                link  = ('http://explosm.net/shorts/random')
            except Exception as e:
                await Util.error_log_command(self.bot,ctx,"randomvideo",error)
                return
            pageSource = str(urllib2.urlopen(link).read()).split()
            for i in pageSource:
                if 'youtube.com/watch' in i:
                    p = i[i.index('"')+1:-1]
                    await ctx.send(embed = embd)
                    await ctx.send(p)
                    return

def setup(bot):
    bot.add_cog(Video(bot))
