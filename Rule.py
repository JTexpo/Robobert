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

class Rule(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        conn = sqlite3.connect('Database.db')
        c = conn.cursor()
        self.roles = c.execute("SELECT role_ID FROM role_table WHERE title = 'RULE';").fetchall()
        conn.close()

    @commands.command(name = 'rule_begins',
                    aliases = ['rule_begin','rb'])
    @Util.is_admin()
    async def rule_begins(self, ctx):
        await Util.log_command(self.bot,ctx,"rule_begins")
        chnl = self.bot.get_channel(Util.RULE_CHNL)
        color = random.randint(0,0xffffff)
        conn = sqlite3.connect('Database.db')
        c = conn.cursor()
        rules = c.execute("SELECT * FROM rule_table;").fetchall()
        conn.close()
        rule_message = "Welcome to the **__Official Cyanide & Happiness Discord Server__**! Let's all have a good time and follow the rules.\n"
        rule_message2 = ""
        rule_message3 = ""
        for rule in range(0,5):
            rule_message += "\n**{}.** {}".format(rules[rule][0],rules[rule][1])
        msg = await chnl.send(embed = discord.Embed(title = "React To This Message To Show You've Read The Rules!",
                description = rule_message,
                colour = color)
                )
        for rule in range(5,12):
            rule_message2 += "\n**{}.** {}".format(rules[rule][0],rules[rule][1])
        msg = await chnl.send(embed = discord.Embed(
                description = rule_message2,
                colour = color)
                )
        for rule in range(12,len(rules)):
            rule_message3 += "\n**{}.** {}".format(rules[rule][0],rules[rule][1])
        rule_message3 += """
        
**To clarify what spam means :**
Sending a message 5 or more times that is a repeat and/or does not contribute to the conversation. Using emotes in a message are fine, but sending singular emotes repeatedly without sending 4 new lines of text may be flagged as spam.

**Meaning of the punishments :**
  __Warn :__ just a slap on the wrist nothing is going to happen just yet.
  __Mute :__ Watch out you need to take a small breather.
  __Kick :__ You're welcome back after you clean up your attitude.
  __Ban :__ Get out of here we don't want your kind."""
        msg = await chnl.send(embed = discord.Embed(
                description = rule_message3,
                colour = color)
                )
        await msg.add_reaction("\U0001F4DD")

    @commands.command(name = 'rule_lookup',
                    aliases = ['rule'])
    async def rule_lookup(self, ctx, rule = 1):
        await Util.log_command(self.bot,ctx,"rule_lookup")
        conn = sqlite3.connect('Database.db')
        c = conn.cursor()
        rule = c.execute("SELECT * FROM rule_table WHERE db_ID = {};".format(rule)).fetchone()
        conn.close()
        await ctx.send(embed = discord.Embed(title = "{} Pulled Up The Rule As A Quick Reference!".format(ctx.author),
                description = "**{}.** {}".format(rule[0],rule[1]),
                colour = random.randint(0,0xffffff))
                )

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if not Util.is_rule_chnl(payload):
            return
        if payload.user_id == self.bot.user.id:
            return
        await self.bot.http.remove_reaction(payload.channel_id, payload.message_id, payload.emoji, payload.user_id)
        user = await self.bot.get_guild(433695004645523456).fetch_member(payload.user_id)
        for role in self.roles:
            await user.add_roles(self.bot.get_guild(433695004645523456).get_role(role[0]))

def setup(bot):
    bot.add_cog(Rule(bot))
