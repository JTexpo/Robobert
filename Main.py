# // -- imports to make the bot work on discord -- //
import discord
from discord.ext import commands
import asyncio
# // -- import for database -- //
import sqlite3
# // -- importing for time -- //
from datetime import datetime
# // -- import the commonly used methods -- //
import Util

# // -- setting up the bot with commands -- //
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="-",case_insensitive=True,intents=intents)

### GETTING STARTED ###
@bot.event
async def on_ready():
    print('------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print(datetime.now())
    print('------')
    for server in bot.guilds:
        print(server.name)
        print(server.id)
        print('------')
    await bot.change_presence(activity=discord.CustomActivity(name = "-help"))

    #bot.loop.create_task(BumpSupport())

### Extensions // Cogs ###
if __name__ == '__main__':
    #bot.remove_command("help")
    extensions = ['Activity','Arcade','Caption','Comic','CTAM','Fun','Info','Mod','Point','Ticket','OWS','Raffle','Rule','Shop','SQL','Video']
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print('Loaded {}'.format(extension))
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension,error))
    bot.loop.create_task(Util.CheckForUpdate(bot))
    bot.loop.create_task(Util.Backup(bot))

@commands.command(name = "load")
@Util.is_admin()
async def load(ctx, extension = ''):
    if extension == '':
        await ctx.send("Please Give A Valid Cog")
    try:
        bot.load_extension(extension)
        await ctx.send('Loaded {}'.format(extension))
    except Exception as error:
        await ctx.send('{} cannot be loaded. [{}]'.format(extension,error))
bot.add_command(load)

@commands.command(name = "unload")
@Util.is_admin()
async def unload(ctx, extension = ''):
    if extension == '':
        await ctx.send("Please Give A Valid Cog")
    try:
        bot.unload_extension(extension)
        await ctx.send('Unloaded {}'.format(extension))
    except Exception as error:
        await ctx.send('{} cannot be unloaded. [{}]'.format(extension,error))
bot.add_command(unload)

@commands.command(name = "reload")
@Util.is_admin()
async def reload(ctx, extension = ''):
    if extension == '':
        await ctx.send("Please Give A Valid Cog")
    try:
        bot.unload_extension(extension)
        bot.load_extension(extension)
        await ctx.send('Reloaded {}'.format(extension))
    except Exception as error:
        await ctx.send('{} cannot be reloaded. [{}]'.format(extension,error))
bot.add_command(reload)

@commands.command(name = 'logout')
@Util.is_admin()
async def logout (ctx):
    await ctx.message.channel.send("Offline...")
    await bot.logout()
bot.add_command(logout)

bot.run(Util.TOKEN[0])
