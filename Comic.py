# // -- imports to make the bot work on discord -- //
import discord
from discord.ext import commands
import asyncio
# // -- import for database -- //
import sqlite3
# // -- import for random decisions -- //
import random
# // -- import for script crawling -- //
import urllib.request as urllib2
from PIL import Image
# // -- import the commonly used methods -- //
import Util


# // -- decorators -- //


class Comic(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        conn = sqlite3.connect('Database.db')
        c = conn.cursor()
        c.execute("SELECT info FROM general_table WHERE title='COMIC-NUMBER';")
        self.max_comic = c.fetchone()
        conn.close()
        self.max_comic = int(self.max_comic[0])

    # // -- Main Comic Command -- //
    @commands.command(name = 'comic')
    @Util.is_comic_chnl()
    async def comic(self,ctx):
        # // -- There are two different types of comics, this will help pick which comic is picked -- //
        if random.randint(0,1) == 1:
            await self.generatecomic.invoke(ctx)
        else:
            await self.randomcomic.invoke(ctx)

    @commands.command(name = 'generatecomic',
                    aliases = ['gc','rcg'])
    @Util.is_comic_chnl()
    async def generatecomic(self,ctx,extension = ''):
        attempt = 0
        link = 'http://explosm.net/rcg/'+extension
        while True:
            await Util.log_command(self.bot,ctx,"generatecomic : {} : {}".format(attempt,extension))
            attempt += 1

            try:
                pageSource = str(urllib2.urlopen(link).read()).split()
            except Exception as error:
                await Util.error_log_command(self.bot,ctx,"generatecomic",error)
                link = 'http://explosm.net/rcg'
                continue
            
            counter = 0
            p = []
            for i in pageSource:
                if "https://rcg-cdn.explosm.net/panels/" in i:
                    p.append(Image.open(urllib2.urlopen(i[i.index('"')+1:i.index('png')]+'png')))
                    counter += 1
                if counter == 3:
                    cpw = Image.open('copyright.png')
                    cpw = cpw.resize((int(cpw.size[0]*.3),int(cpw.size[1]*.3)), Image.ANTIALIAS)
                    new_image = Image.new('RGB',(3*p[0].size[0],p[0].size[1]), (250,250,250))
                    new_image.paste(p[0],(0,0))
                    new_image.paste(p[1],(p[0].size[0],0))
                    new_image.paste(p[2],(2*p[0].size[0],0))
                    new_image.paste(cpw,(int((3*p[0].size[0] - cpw.size[0])/2),p[0].size[1] - cpw.size[1]))
                    new_image.save("generated_comic.png","png")
                    for x in pageSource:
                        if "explosm.net/rcg/" in x:
                            l = x[x.index('"')+1:x.index('"')+1+x[x.index('"')+1:].index('"')]
                            break
                    embd = discord.Embed (title = "Random Comic Generator",
                            description = "A comic generated by **{}**!\nPeramilink: [Click Here]({})\nMake Your Own: [Click Here]({})".format(ctx.message.author.name,l,'http://explosm.net/rcg'),
                            colour = random.randint(0,0xffffff))
                    file = discord.File("generated_comic.png", filename="generated_comic.png")
                    embd.set_image(url="attachment://generated_comic.png")
                    embd.set_thumbnail(url = ctx.message.author.avatar_url)
                    embd.set_footer(text = "Extension: {}".format(l[-9:]))
                    await ctx.send(file=file,embed = embd)
                    return

    @commands.command(name = 'randomcomic',
                    aliases = ['rc','rob','matt','dave','kris'])
    @Util.is_comic_chnl()
    async def randomcomic(self, ctx, number = 0):
        if number == 0: number = random.randint(615,self.max_comic)
        attempt  = 0
        athr = "NaN"
        role = "NaN"
        if 'kris' in ctx.message.content.lower() :
            athr = 'Kris Wilson'
            role = "KRIS"
        elif 'matt'in ctx.message.content.lower() :
            athr = 'Matt Melvin'
            role = "MATT"
        elif 'rob' in ctx.message.content.lower() :
            athr = 'Rob DenBleyker'
            role = "ROB"
        elif 'dave' in ctx.message.content.lower() :
            athr = 'Dave McElfatrick'
            role = "DAVE"

        if role != "NaN":
            conn = sqlite3.connect('Database.db')
            c = conn.cursor()
            c.execute("SELECT role_ID FROM role_table WHERE title='{}';".format(role))
            role = c.fetchone()
            conn.close()
            await ctx.author.add_roles(ctx.guild.get_role(role[0]))

        while True:
            await Util.log_command(self.bot,ctx,"randomcomic : {} : {}".format(attempt,number))
            attempt += 1
            if attempt > 1:
                number = random.randint(615,self.max_comic)
            try:
                pageSource = str(urllib2.urlopen('http://explosm.net/comics/{}'.format(number)).read()).split()
            except Exception as error:
                await Util.error_log_command(self.bot,ctx,"randomcomic : {}".format(number),error)
                continue

            link = Util.getComic(pageSource)
            if link != "NaN":
                author,avatar,number = Util.getComicInfo(pageSource)
                if (athr != 'NaN' and athr != author):
                    number = random.randint(615,self.max_comic)
                    continue
                embd = discord.Embed(title = "A Random Comic Was Found",
                        description = ("A comic created by **{}**!\nIf you like what you see checkout more on our website: [Explosm.net](http://explosm.net)".format(author)),
                        colour = random.randint(0,0xffffff))
                embd.set_thumbnail(url = str(avatar))
                embd.set_image(url = 'http://'+str(link))
                embd.set_footer(text = "Comic Number : {}".format(number))
                await ctx.send(embed = embd)
                return

def setup(bot):
    bot.add_cog(Comic(bot))
