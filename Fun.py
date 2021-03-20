# // -- imports to make the bot work on discord -- //
import discord
from discord.ext import commands
import asyncio
# // -- import for database -- //
import sqlite3
# // -- import for random decisions -- //
import random

import time
# // -- import the commonly used methods -- //
import Util

def is_JTexpo():
    def predicate(ctx):
        return int(ctx.author.id) == int(319199396724211722)
    return commands.check(predicate)

class Fun(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        conn = sqlite3.connect('Database.db')
        c = conn.cursor()
        c.execute("SELECT info FROM general_table WHERE title='HISTORY-LOG-EMOJI';")
        self.history_log_emoji = c.fetchone()
        c.execute("SELECT channel_ID FROM channel_table WHERE title='HISTORY-LOG';")
        self.history_log_chnl = c.fetchone()
        conn.close()
        self.history_log_emoji = int(self.history_log_emoji[0])

    @commands.command(name = 'echo')
    @is_JTexpo()
    async def echo(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command(name = 'dick',
                    aliases = ['size'])
    @commands.cooldown(1, 300, commands.BucketType.user)
    @Util.fun_pass()
    async def dick(self, ctx):
        await Util.log_command(self.bot,ctx,"dick")
        message = "<:dick_4:699753071760113796>"
        rng = random.randint(1,3)
        while rng != 1:
            if rng == 3:
                message += "<:dick_3:699753105344167936>"
            elif rng == 2:
                message += "<:dick_2:699753137367547964>"
            rng = random.randint(1,3)
        message += "<:dick_1:699753154815721562>"
        await ctx.send(message)

    @commands.command(name = "jumbo")
    @commands.cooldown(1, 300, commands.BucketType.user)
    @Util.fun_pass()
    async def jumbo(self,ctx,emoji:discord.PartialEmoji = None):
        await Util.log_command(self.bot,ctx,"jumbo")
        if not emoji:
            return
        embed = discord.Embed(colour = random.randint(0,0xffffff))
        embed.set_image(url = str(emoji.url))
        await ctx.send(embed = embed)

    @commands.command(name = 'respect',
                    aliases = ['f'])
    @commands.cooldown(1, 300, commands.BucketType.user)
    @Util.fun_pass()
    async def respect(self, ctx):
        await Util.log_command(self.bot,ctx,"respect")
        rng = random.randint(0,5)
        embed = discord.Embed(title = "{} Paid Their Respect".format(ctx.author.name),
                description = "{} out of 5 F's were given.\n".format(rng)+"<:FBomb:700508120891523173>"*rng+":boom:"*(5-rng),
                colour = random.randint(0,0xffffff)
                )
        await ctx.send(embed = embed)


    @commands.command(name = "trolley")
    @commands.cooldown(1, 300, commands.BucketType.user)
    @Util.fun_pass()
    async def trolley (self,ctx, arg1 = "this_stuff", arg2 = "that__stuff"):
        await Util.log_command(self.bot,ctx,"trolley")
        def check(member,voters):
            try:
                vote = voters[member]
                return vote
            except:
                return None


        def embed():
            embed = discord.Embed(title = "Oh Dear Oh Me, It Looks Like There's Stuff On The Tracks Again",
                              description = "Oh wont you help dear old Tom and vote for which path I should go?\nVote by reacting:\n\U00002B05 for {}\n\U000027A1 for {}".format(arg1,arg2),
                              colour = random.randint(0,0xffffff))
            embed.set_image(url = "https://robobert.tobira.io/images/fun-commands/trolley-welcome.gif")
            #embed.set_thumbnail(url = ctx.message.author.avatar_url)
            return embed

        left = 0
        right = 0
        voters = {}

        poll = embed()
        poll.add_field(name = "In Favor To Hit {}".format(arg1), value = "{}".format(left),inline = True)
        poll.add_field(name = "In Favor To Hit {}".format(arg2), value = "{}".format(right),inline = True)

        msg = await ctx.send(embed = poll)
        await msg.add_reaction('\U00002B05')
        await msg.add_reaction('\U000027A1')
        await asyncio.sleep(1)

        def rcheck(reaction,user):
            return int(reaction.message.id) == int(msg.id)

        start = time.time()
        while ((time.time() - start) < 30):
            try:
                reaction, user = await self.bot.wait_for('reaction_add',check = rcheck,timeout = 1)
            except:
                continue
            await msg.remove_reaction(emoji=reaction.emoji,member=user)
            if (reaction.emoji == "\U00002B05"):
                hasvote = check(user,voters)
                if hasvote == 'left':
                    continue
                elif hasvote == 'right':
                    right -= 1
                    left += 1
                    voters[user] = 'left'
                else:
                    voters.update({user:'left'})
                    left += 1
            elif (reaction.emoji == "\U000027A1"):
                hasvote = check(user,voters)
                if hasvote == 'right':
                    continue
                elif hasvote == 'left':
                    right += 1
                    left -= 1
                    voters[user] = 'right'
                else:
                    voters.update({user:'right'})
                    right += 1
            poll = embed()
            poll.add_field(name = "In Favor To Hit {}".format(arg1), value = "{}".format(left),inline = True)
            poll.add_field(name = "In Favor To Hit {}".format(arg2), value = "{}".format(right),inline = True)

            await msg.edit(embed = poll)

        death = arg1 if left > right else arg2

        embd = discord.Embed(title = "Oh No!",
                            description = "Looks like poor {} could not get out of the way".format(death),
                            colour = random.randint(0,0xffffff))
        embd.set_image(url = "https://robobert.tobira.io/images/fun-commands/single-hit.gif")

        if left == right:
            embd = discord.Embed(title = "Oh No!",
                            description = "Looks likes both {} and {} could not get out of the way".format(arg1,arg2),
                            colour = random.randint(0,0xffffff))
            embd.set_image(url = "https://robobert.tobira.io/images/fun-commands/trolley-drift.gif")

        await msg.edit(embed = embd)

    async def fun_embed(self, ctx, header, descript, image):
        embed = discord.Embed(title = header,
                description = descript,
                colour = random.randint(0,0xffffff)
                )
        embed.set_image(url = image)
        embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = embed)

    @commands.command(name = 'mute')
    @commands.cooldown(1, 300, commands.BucketType.user)
    @Util.fun_pass()
    async def mute(self, ctx, target: discord.Member = None, *,reason = "none"):
        await Util.log_command(self.bot,ctx,"mute")
        head = "{} Is Asking Everyone To Be Quiet!".format(ctx.author.name) if target == None else "{} Is Asking {} To Be Quiet For Once In Their Life!".format(ctx.author.name,target.name)
        desc = "I hope metal tastes nice because Lunk's hushing you up." if reason == "none" else "I hope metal tastes nice because Lunk's hushing you up.\n**Reason :** {}".format(reason)
        image = "https://robobert.tobira.io/images/fun-commands/mute.gif"
        await self.fun_embed(ctx,head,desc,image)
    
    @commands.command(name = 'sip')
    @commands.cooldown(1, 300, commands.BucketType.user)
    @Util.fun_pass()
    async def mute(self, ctx, target: discord.Member = None, *,reason = "none"):
        await Util.log_command(self.bot,ctx,"sip")
        head = "{} Is Just Taking a Sip...".format(ctx.author.name) if target == None else "{} Is Just Taking a Sip With {}...".format(ctx.author.name,target.name)
        desc = "hmmmmmmm..." if reason == "none" else "Oh... Well... this is weird.\n**Reason :** {}".format(reason)
        image = "https://robobert.tobira.io/images/fun-commands/sip.gif"
        await self.fun_embed(ctx,head,desc,image)

    @commands.command(name = 'ban')
    @commands.cooldown(1, 300, commands.BucketType.user)
    @Util.fun_pass()
    async def ban(self, ctx, target: discord.Member = None, *,reason = "none"):
        await Util.log_command(self.bot,ctx,"ban")
        head = "{} Is Dropping The Ban Hammer On Everyone!".format(ctx.author.name) if target == None else "{} Is Banning {} Back To The Shadow Realm!".format(ctx.author.name,target.name)
        desc = "The belt is comming off, and it's time for a banning!" if reason == "none" else "The belt is comming off, and it's time for a banning!\n**Reason :** {}".format(reason)
        image = "https://robobert.tobira.io/images/fun-commands/ban.gif"
        await self.fun_embed(ctx,head,desc,image)

    @commands.command(name = 'kick')
    @commands.cooldown(1, 300, commands.BucketType.user)
    @Util.fun_pass()
    async def kick(self, ctx, target: discord.Member = None, *,reason = "none"):
        await Util.log_command(self.bot,ctx,"kick")
        head = "{} Is Kicking Everyone From The Friend Circle!".format(ctx.author.name) if target == None else "{} Is Kicking {} From The Friend Circle!".format(ctx.author.name,target.name)
        desc = "Go get your own food, you smelly dog you." if reason == "none" else "Go get your own food, you smelly dog you.\n**Reason :** {}".format(reason)
        image = "https://robobert.tobira.io/images/fun-commands/kick.gif"
        await self.fun_embed(ctx,head,desc,image)

    @commands.command(name = 'hug')
    @commands.cooldown(1, 300, commands.BucketType.user)
    @Util.fun_pass()
    async def hug(self, ctx, target: discord.Member = None, *,reason = "none"):
        await Util.log_command(self.bot,ctx,"hug")
        head = "{} Is Sharing The Love With Everyone!".format(ctx.author.name) if target == None else "{} Is Going To Make All Your Problems Go Away, {}!".format(ctx.author.name,target.name)
        desc = "Get in close, cause big hug bill is here." if reason == "none" else "Get in close, cause big hug bill is here.\n**Reason :** {}".format(reason)
        image = "https://robobert.tobira.io/images/fun-commands/hug.gif"
        await self.fun_embed(ctx,head,desc,image)

    @commands.command(name = 'unmute')
    @commands.cooldown(1, 300, commands.BucketType.user)
    @Util.fun_pass()
    async def unmute(self, ctx, target: discord.Member = None, *,reason = "none"):
        await Util.log_command(self.bot,ctx,"unmute")
        head = "{} Is Allowing Everyone To Speak!".format(ctx.author.name) if target == None else "{} Is Letting {} Speak Again!".format(ctx.author.name,target.name)
        desc = "Lunk has removed the muted shield, speak now or forever hold your peace." if reason == "none" else "Lunk has removed the muted shield, speak now or forever hold your peace.\n**Reason :** {}".format(reason)
        image = "https://robobert.tobira.io/images/fun-commands/unmute.gif"
        await self.fun_embed(ctx,head,desc,image)


    @commands.Cog.listener()
    async def on_reaction_add(self, ctx, user):
        try:
            mychn = self.bot.get_channel(int(self.history_log_chnl[0]))
            if ((ctx.emoji.id == self.history_log_emoji) and
                (ctx.count == 3) and
                (ctx.message.channel != mychn) and
                (not(ctx.message.id in Util.HIGHLIGHT_HIST))
                ):
                embed = discord.Embed(description = "{}\n\nClick Here To Read For Yourself : [Link]({})".format(
                            ctx.message.content,ctx.message.jump_url),
                        colour = random.randint(0,0xffffff)
                        )
                embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
                Util.HIGHLIGHT_HIST.append(ctx.message.id)
                await mychn.send(embed = embed)
        except Exception as error:
            return




def setup(bot):
    bot.add_cog(Fun(bot))
