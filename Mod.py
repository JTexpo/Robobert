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

class Mod(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        conn = sqlite3.connect('Database.db')
        c = conn.cursor()
        c.execute("SELECT channel_ID FROM channel_table WHERE title='MUTE-LOG';")
        self.mutelog = c.fetchone()
        c.execute("SELECT info FROM general_table WHERE title='MOD-LOG-EMOJI';")
        self.mod_log_emoji = c.fetchone()
        c.execute("SELECT channel_ID FROM channel_table WHERE title='PUBLIC-MOD-LOG';")
        self.publ_mod_chnl = c.fetchone()
        conn.close()
        self.mod_log_emoji = int(self.mod_log_emoji[0])

    # // -- ALL OF THE CLEARS -- //
    @commands.command(name = 'clear',
                    aliases = ['purge','clean'])
    @Util.is_admin()
    async def clear(self, ctx, amount = 5):
        await Util.log_command(self.bot,ctx,"clear")
        await ctx.message.delete()
        if amount > 100 or amount < 0:
            return await ctx.send("Invalid amount.Maximum is 100.")
        deleted = await ctx.channel.purge(limit = amount)
        await ctx.send(embed = discord.Embed(title = ':thumbsup: Deleted **{}/{}** possible messages for you.'.format(len(deleted),amount)),delete_after=10)


    @commands.command(name = 'clearemote',
                    aliases = ['purgeemote','cleanemote','clearemotes','purgeemotes','cleanemotes'])
    @Util.is_admin()
    async def clearemote(self, ctx, amount = 5):
        await Util.log_command(self.bot,ctx,"clearemote")
        await ctx.message.delete()
        deleted = 0
        saveamount = amount
        msgList = []
        if amount > 100 or amount < 0:
            return await ctx.send("Invalid amount.Maximum is 100.")
        async for msg in ctx.channel.history(limit = 1000):
            if amount <= 0:
                break
            if msg.content.startswith("<") or msg.content.endswith(">"):
                amount -= 1
                deleted += 1
                msgList.append(msg)
        await ctx.channel.delete_messages(msgList)
        await ctx.send(embed = discord.Embed(title = ':thumbsup: Deleted **{}/{}** possible messages for you.'.format(deleted,saveamount)),delete_after=10)


    @commands.command(name = 'clearuser',
                    aliases = ['purgeuser','cleanuser','clearusers','purgeusers','cleanusers'])
    @Util.is_admin()
    async def clearuser(self, ctx, target: discord.Member = None, amount = 5):
        await Util.log_command(self.bot,ctx,"clearuser")
        await ctx.message.delete()
        saveamount = amount
        deleted = 0
        msgList = []
        if amount > 100 or amount < 0:
            return await ctx.send("Invalid amount.Maximum is 100.")
        async for msg in ctx.channel.history(limit = 1000):
            if amount <= 0:
                break
            if msg.author.id == target.id:
                amount -= 1
                deleted += 1
                msgList.append(msg)
        await ctx.channel.delete_messages(msgList)
        await ctx.send(embed = discord.Embed(title = ':thumbsup: Deleted **{}/{}** possible messages for you.'.format(deleted,saveamount)),delete_after=10)


    @commands.command(name = 'clearonly',
                    aliases = ['purgeonly','cleanonly'])
    @Util.is_admin()
    async def clearonly(self, ctx, txt = '', amount = 5):
        await Util.log_command(self.bot,ctx,"clearonly")
        await ctx.message.delete()
        deleted = 0
        saveamount = amount
        onlyStart = False
        msgList = []
        if txt[0] == '^':
            onlyStart = True
        async for msg in ctx.channel.history(limit = 1000):
            if amount <= 0:
                break
            if onlyStart and msg.content.lower().startswith(txt[1:].lower()):
                amount -= 1
                await msg.delete()
                deleted += 1
            elif txt.lower() in msg.content.lower():
                amount -= 1
                deleted += 1
                msgList.append(msg)
        await ctx.channel.delete_messages(msgList)
        await ctx.send(embed = discord.Embed(title = ':thumbsup: Deleted **{}/{}** possible messages for you.'.format(deleted,saveamount)),delete_after=10)

    # // -- MUTE BEGGING -- //
    @commands.command(name = 'mutebegging',
                    aliases = ['mb','mute_begging'])
    @Util.is_admin()
    async def mutebegging(self, ctx, *, note = ''):
        await Util.log_command(self.bot,ctx,"mutebegging")
        mycontent = ''
        async for msg in ctx.channel.history(limit = 10000):
            mycontent += "\n{} : {} : {}".format(msg.created_at,msg.author,msg.content)
        extension = Util.html_log('mute-begging',mycontent,ctx.channel.name,ctx.message.id)
        mychn = self.bot.get_channel(int(self.mutelog[0]))
        embed = discord.Embed(title = "Mute Begging Reset",
                description = "Mute Begging has been reset by {}\nReason : {}\nFor more details visit : https://robobert.tobira.io/mute-begging/{}".format(
                    ctx.author,
                    note,
                    (extension+"mute-begging-{}.txt".format(ctx.message.id))
                    ),
                colour = random.randint(0,0xffffff)
                )
        await ctx.channel.purge(limit = 100)
        await mychn.send(embed = embed)
        embed = discord.Embed(title = "__Mute Begging Guide :__",
                              description = """**If You Are Reading This, You Are Muted. Below Are Some Reasons Of Why This Happened:**
 - __Breaking The Rules__ : Please take a step back and ask yourself if you broke any rules, and if the mute was justified.
 - __Sending Too Many Lines__ : Aperture will auto mute you if you are sending too many new lines at once, this is meant for spam detection.
 - __Caught Being A Troll In The Gaming Channels__ : If this applies to you, lucky you can still type in other channels just not the gaming ones.

 **If You Want To Be Unmuted:**
 - Please Ping An Online Mod
 - Please Wait Out The Mute Respectfully If Your Request Is Denied

We mods are here to help enforce the rules that Cyanide and Happiness has laid out that they wanted in their server. If you continue to repeat offend, than that may result in a ban. This servers goal is to be a welcoming environment for everyone.
""",
                              colour = random.randint(0,0xffffff))
        embed.set_footer(text = "Arguing with a mod will not help your case")
        await ctx.send(embed = embed)

    @commands.command(name = 'mod_mute',
                    aliases = ['modmute'])
    @Util.is_admin()
    async def mod_mute(self, ctx, target: discord.Member = None, *, note = ''):
        await Util.log_command(self.bot,ctx,"mod_mute")
        try:
            await target.add_roles(ctx.guild.get_role(568100605160062994))
            modchan = self.bot.get_channel(568088139453825049)
            await modchan.send(embed = discord.Embed(title = "{} muted {}".format(ctx.author,target),description = ("{}".format(note)),colour = random.randint(0,0xffffff)))
        except Exception as error:
            await Util.error_log_command(self.bot,ctx,'mod_mute',error)

    @commands.command(name = 'mod_unmute',
                    aliases = ['modunmute'])
    @Util.is_admin()
    async def mod_unmute(self, ctx, target: discord.Member = None, *, note = ''):
        await Util.log_command(self.bot,ctx,"mod_unmute")
        try:
            await target.remove_roles(ctx.guild.get_role(568100605160062994))
            modchan = self.bot.get_channel(568088139453825049)
            await modchan.send(embed = discord.Embed(title = "{} unmuted {}".format(ctx.author,target),description = ("{}".format(note)),colour = random.randint(0,0xffffff)))
        except Exception as error:
            await Util.error_log_command(self.bot,ctx,'mod_unmute',error)

    @commands.command(name = 'mod_kick',
                    aliases = ['modkick'])
    @Util.is_admin()
    async def mod_kick(self, ctx, target: discord.Member = None, *, note = ''):
        await Util.log_command(self.bot,ctx,"mod_kick")
        try:
            await target.kick(reason = note)
            modchan = self.bot.get_channel(568088139453825049)
            await modchan.send(embed = discord.Embed(title = "{} kick {}".format(ctx.author,target),description = ("{}".format(note)),colour = random.randint(0,0xffffff)))
        except Exception as error:
            await Util.error_log_command(self.bot,ctx,'mod_kick',error)

    @commands.command(name = 'mod_ban',
                    aliases = ['modban'])
    @Util.is_admin()
    async def mod_ban(self, ctx, target: discord.Member = None, *, note = ''):
        await Util.log_command(self.bot,ctx,"mod_ban")
        try:
            await target.ban(reason = note)
            modchan = self.bot.get_channel(568088139453825049)
            await modchan.send(embed = discord.Embed(title = "{} banned {}".format(ctx.author,target),description = ("{}".format(note)),colour = random.randint(0,0xffffff)))
        except Exception as error:
            await Util.error_log_command(self.bot,ctx,'mod_ban',error)



    @commands.Cog.listener()
    async def on_message(self, ctx):
        if not Util.is_apt_chnl(ctx):
            return
        if 'mute' in ctx.content:
            mchannel = self.bot.get_channel(Util.MUTE_BEGGING_CHNL[0])
            await mchannel.send(embed = discord.Embed(description = ("{}".format(ctx.content)),colour = random.randint(0,0xffffff)))

    @commands.Cog.listener()
    async def on_reaction_add(self, ctx, user):
        try:
            if ctx.emoji.id == self.mod_log_emoji:
                if ctx.count == 2:
                    embed = discord.Embed(description = "{}\n\nClick Here To Read For Yourself : [Link]({})".format(
                                ctx.message.content,ctx.message.jump_url),
                            colour = random.randint(0,0xffffff)
                            )
                    embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
                    mychn = self.bot.get_channel(int(self.publ_mod_chnl[0]))
                    await mychn.send(embed = embed)
        except Exception as error:
            return

def setup(bot):
    bot.add_cog(Mod(bot))
