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

class OWS(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.activity = {}
        conn = sqlite3.connect('Database.db')
        c = conn.cursor()
        c.execute("SELECT channel_ID FROM channel_table WHERE title='ONE-WORD-LOG';")
        self.ows_log = c.fetchone()
        conn.close()

    # @commands.command(name = 'end',aliases = ['theend'])
    async def end(self, ctx):
        #await Util.log_command(self.bot,ctx,"end")
        #await ctx.message.delete()
        color = random.randint(0,0xffffff)
        story = []
        activity = {}
        purge_amount = 0
        async for msg in ctx.channel.history(limit = 10000):
            purge_amount += 1
            story.append(msg.content)
            if msg.author.id in activity:
                activity[msg.author.id] += 1
            else:
                activity[msg.author.id] = 1
            if msg.content.lower() in ['mario','joel','voldemort','bird']:
                conn = sqlite3.connect('Database.db')
                c = conn.cursor()
                c.execute("SELECT role_ID FROM role_table WHERE title='{}';".format(msg.content.upper()))
                role = c.fetchone()
                conn.close()
                if role == None:
                    continue
                try:
                    await msg.author.add_roles(msg.channel.guild.get_role(role[0]))
                except Exception as error:
                    await Util.error_log_command(self.bot,ctx,"OWS",error)
        story.reverse()
        story = ' '.join(story)
        while purge_amount > 0:
            await ctx.channel.purge(limit = 100)
            purge_amount -= 100
            await asyncio.sleep(3)

        mychn = self.bot.get_channel(int(self.ows_log[0]))
        embed = discord.Embed(title = "A Story Made By The Community!",
                description = story,
                colour = color
                )
        await mychn.send(embed = embed)

        activity = sorted(activity.items(), key = lambda kv: kv[1])
        activity.reverse()
        embed = discord.Embed(title = "Members That Helped Create The Story!",
            colour = color
            )
        for user in activity:
            try:
                member = await ctx.guild.fetch_member(user[0])
            except:
                continue
            embed.add_field(name = "{}".format(member), value = "Wrote {} Words!".format(user[1]))
        await mychn.send(embed = embed)

        embed = discord.Embed(title = "Welcome To One Word Story!",
                description = """**Rules :**
To make sure that everyone has fun, we have a few rules in place. Not following the rules will cause you to lose your premission to this channel, so please read the rules.
**1.** READ THE CHAT LOG BEFORE POSTING!
**2.** Please Make Sure Your Post Make Sense.
**3.** No Trolling.
**4.** Do Not Abuse Reactions.
--
Other thing you should note is that every message will have 2 reactions. When three people click on the 'X' the message will be deleted, and when 3 people click on the 'loudspeaker' the message will be published and logged.
""",
                colour = color
                )
        await ctx.channel.send(embed = embed)

    @commands.command(name = 'mod_end',
                    aliases = ['modend','mend'])
    @Util.is_admin()
    async def mod_end(self, ctx):
        await Util.log_command(self.bot,ctx,"mod_end")
        await ctx.message.delete()
        await self.end(ctx)

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if not Util.is_ows_chnl(ctx):
            return
        if ctx.author.id == self.bot.user.id:
            return
        if len(ctx.content.split()) > 1:
            await ctx.delete()
        prev = await ctx.channel.history(limit = 2).flatten()
        try:
            if int(prev[0].author.id) == int(prev[1].author.id):
                await ctx.delete()
        except:
            pass
        await ctx.add_reaction("\U0000274E")
        await ctx.add_reaction("\U0001F4E2")


    @commands.Cog.listener()
    async def on_reaction_add(self, ctx, user):
        if not Util.is_ows_chnl(ctx.message):
            return
        all_reacts = ctx.message.reactions
        try:
            if all_reacts[0].count == 3:
                await ctx.message.delete()
            elif all_reacts[1].count == 3:
                await self.end(ctx.message)
        except Exception as error:
            return

def setup(bot):
    bot.add_cog(OWS(bot))
