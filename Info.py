# // -- imports to make the bot work on discord -- //
import discord
from discord.ext import commands
import asyncio
# // -- import for random decisions -- //
import random
# // -- import for script crawling -- //
import urllib.request as urllib2
# // -- import the commonly used methods -- //
import Util

class Info(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name = "ping")
    async def ping(self,ctx):
        await ctx.send('Pong! {0} ms'.format(round(self.bot.latency*1000)))

    @commands.command(name = "info")
    async def info(self, ctx, target: discord.Member = None):
        await Util.log_command(self.bot,ctx,"info")
        if target == None : target = ctx.author

        embed = discord.Embed(title = "information on {} : {}".format(target.name, target.id),
            description = "This Is All Public Information That Discord Stores",
            colour = random.randint(0,0xffffff)
            )
        embed.add_field(name = "Name", value = target.name, inline = False)
        embed.add_field(name = "Nickname", value = target.nick, inline = False)
        embed.add_field(name = "ID", value = target.id, inline = False)
        embed.add_field(name = "Status", value = target.status, inline = False)
        embed.add_field(name = "Bot?", value = target.bot, inline = False)
        embed.add_field(name = "Created On", value = target.created_at, inline = False)
        embed.add_field(name = "Joined On", value = target.joined_at, inline = False)
        embed.add_field(name = "Booster Since", value = target.premium_since, inline = False)
        embed.add_field(name = "Role Count", value = len(target.roles), inline = False)
        embed.add_field(name = "Top Role", value = target.top_role, inline = False)

        embed.set_thumbnail(url = target.avatar_url)

        await ctx.send(embed = embed)

    @commands.command(name = "channel")
    async def channel(self, ctx, target = None):
        await Util.log_command(self.bot,ctx,"channel")
        if target == None : target = ctx.channel

        embed = discord.Embed(title = "information on {} : {}".format(target.name, target.id),
            description = "This Is All Public Information That Discord Stores",
            colour = random.randint(0,0xffffff)
            )

        embed.add_field(name = "Name", value = target.name, inline = False)
        embed.add_field(name = "ID", value = target.id, inline = False)
        embed.add_field(name = "Type", value = target.type, inline = False)
        embed.add_field(name = "Created On", value = target.created_at, inline = False)
        embed.add_field(name = "Server", value = target.guild, inline = False)
        embed.add_field(name = "Position", value = target.position, inline = False)
        embed.add_field(name = "NSFW?", value = target.is_nsfw(), inline = False)

        await ctx.send(embed = embed)

    @commands.command(name = "server")
    async def server(self, ctx):
        await Util.log_command(self.bot,ctx,"server")
        target = ctx.guild

        embed = discord.Embed(title = "information on {} : {}".format(target.name, target.id),
            description = "This Is All Public Information That Discord Stores",
            colour = random.randint(0,0xffffff)
            )

        embed.add_field(name = "Name", value = target.name, inline = False)
        embed.add_field(name = "ID", value = target.id, inline = False)
        embed.add_field(name = "Created On", value = target.created_at, inline = False)
        embed.add_field(name = "Description", value = target.description, inline = False)
        embed.add_field(name = "Verification Level", value = target.verification_level, inline = False)
        embed.add_field(name = "Owner", value = target.owner.name, inline = False)
        embed.add_field(name = "Owner ID", value = target.owner_id, inline = False)
        embed.add_field(name = "Region", value = target.region, inline = False)
        embed.add_field(name = "Member Count", value = target.member_count, inline = False)
        embed.add_field(name = "Emoji Count", value = len(target.emojis), inline = False)
        embed.add_field(name = "Category Count", value = len(target.categories), inline = False)
        embed.add_field(name = "Channel Count", value = len(target.channels), inline = False)
        embed.add_field(name = "Role Count", value = len(target.roles), inline = False)
        embed.add_field(name = "Nitro Level", value = target.premium_tier, inline = False)
        embed.add_field(name = "Nitro Boost", value = target.premium_subscription_count, inline = False)
        embed.add_field(name = "Nitro Boosters", value = len(target.premium_subscribers), inline = False)
        embed.add_field(name = "Max Presences", value = target.max_presences, inline = False)
        embed.add_field(name = "Max Members", value = target.max_members, inline = False)
        embed.add_field(name = "MFA Level", value = target.mfa_level, inline = False)
        embed.add_field(name = "Emoji Limit", value = target.emoji_limit, inline = False)
        embed.add_field(name = "Bit Rate Limit", value = target.bitrate_limit, inline = False)
        embed.add_field(name = "File Size Limit", value = target.filesize_limit, inline = False)

        embed.set_thumbnail(url = target.icon_url)
        embed.set_image(url = target.banner_url)

        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Info(bot))
