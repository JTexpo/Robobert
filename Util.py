# // -- imports to make the bot work on discord -- //
import discord
from discord.ext import commands
import asyncio
# // -- import for os edits -- //
import os
# // -- import for database -- //
import sqlite3
# // -- import for random color -- //
import random
# // -- import for script crawling -- //
import urllib.request as urllib2
# // -- import for time of day -- //
from datetime import datetime
from datetime import date
# // -- Global Varibles Keep As Small As Possible -- //
ACTIVITY = {}
POINT = {}
RAFFLE = []
HIGHLIGHT_HIST = []
# // -- getting the token from the database -- //
conn = sqlite3.connect('Database.db')
c = conn.cursor()

c.execute("SELECT channel_ID FROM channel_table WHERE title='LOG';")
LOG = c.fetchone()
c.execute("SELECT info FROM general_table WHERE title='TOKEN';")
TOKEN = c.fetchone()
c.execute("SELECT admin_ID FROM admin_table;")
ADMINS = c.fetchall()
c.execute("SELECT channel_ID FROM channel_table WHERE title='POINT-EARN-CHANNEL';")
POINT_CHNLS = c.fetchall()
c.execute("SELECT channel_ID FROM channel_table WHERE title='COMIC-CHANNEL';")
COMIC_CHNLS = c.fetchall()
c.execute("SELECT channel_ID FROM channel_table WHERE title='CTAM-CHANNEL';")
CTAM_CHNL = c.fetchone()
c.execute("SELECT channel_ID FROM channel_table WHERE title='ARCADE-CHANNEL';")
ARCADE_CHNL = c.fetchone()
c.execute("SELECT channel_ID FROM channel_table WHERE title='MOD-ACTION';")
MOD_ACTION_CHNL = c.fetchone()
c.execute("SELECT user_ID, message_count FROM activity_table;")
DB_ACTIVITY = c.fetchall()
c.execute("SELECT user_ID, points FROM point_table;")
DB_POINT = c.fetchall()
c.execute("SELECT user_ID FROM raffle_table;")
DB_RAFFLE = c.fetchall()
c.execute("SELECT channel_ID FROM channel_table WHERE title='MUTE-BEGGING';")
MUTE_BEGGING_CHNL = c.fetchone()
c.execute("SELECT channel_ID FROM channel_table WHERE title='TICKET-CATEGORY';")
TICKET_CAT = c.fetchone()
c.execute("SELECT channel_ID FROM channel_table WHERE title='RAFFLE-CHANNEL';")
RAFFLE_CHNL = c.fetchone()
c.execute("SELECT channel_ID FROM channel_table WHERE title='HELP-DESK';")
HELP_CHNL = c.fetchone()
c.execute("SELECT channel_ID FROM channel_table WHERE title='RULE';")
RULE_CHNL = c.fetchone()
c.execute("SELECT channel_ID FROM channel_table WHERE title='SHOP-CHANNEL';")
SHOP_CHNL = c.fetchone()
c.execute("SELECT channel_ID FROM channel_table WHERE title='ONE-WORD-CHANNEL';")
OWS = c.fetchone()
c.execute("SELECT info FROM general_table WHERE title='CTAM-SCORE';")
COUNT = c.fetchone()
c.execute("SELECT info FROM general_table WHERE title='CTAM-HIGH-SCORE';")
COUNT_HIGH = c.fetchone()

conn.close()

COUNT = int(COUNT[0])
COUNT_HIGH = int(COUNT_HIGH[0])
ARCADE_CHNL = int(ARCADE_CHNL[0])
TICKET_CAT = int(TICKET_CAT[0])
HELP_CHNL = int(HELP_CHNL[0])
RULE_CHNL = int(RULE_CHNL[0])
SHOP_CHNL = int(SHOP_CHNL[0])
RAFFLE_CHNL = int(RAFFLE_CHNL[0])

# // -- Decorators -- //
def is_admin():
    def predicate(ctx):
        for admin in ADMINS:
            if int(admin[0]) == int(ctx.author.id):
                return True
        return False
    return commands.check(predicate)

def is_comic_chnl():
    def predicate(ctx):
        for chnl in COMIC_CHNLS:
            if int(chnl[0]) == int(ctx.channel.id):
                return True
        return False
    return commands.check(predicate)

def is_mute_begging():
    def predicate(ctx):
        return int(ctx.channel.id) == int(MUTE_BEGGING_CHNL)
    return commands.check(predicate)

def is_chn_in_tick():
    def predicate(ctx):
        return int(ctx.channel.category_id) == int(TICKET_CAT)
    return commands.check(predicate)

def is_help_desk(ctx):
    return int(ctx.channel_id) == int(HELP_CHNL)

def is_rule_chnl(ctx):
    return int(ctx.channel_id) == int(RULE_CHNL)

def is_raffle_chnl(ctx):
    return int(ctx.channel_id) == int(RAFFLE_CHNL)

def is_point_chnl(ctx):
    for chnl in POINT_CHNLS:
        if int(chnl[0]) == int(ctx.channel.id):
            return True
    return False

def is_arcade_chnl():
    def predicate(ctx):
        return int(ctx.channel.id) == int(ARCADE_CHNL)
    return commands.check(predicate)

def is_shop_chnl():
    def predicate(ctx):
        return int(ctx.channel.id) == int(SHOP_CHNL)
    return commands.check(predicate)

def is_ows_chnl(ctx):
    return int(ctx.channel.id) == int(OWS[0])
def a_ows_chnl():
    def predicate(ctx):
        return int(ctx.channel.id) == int(OWS[0])
    return commands.check(predicate)

def is_ctam_chnl(ctx):
    return int(ctx.channel.id) == int(CTAM_CHNL[0])
def a_ctam_chnl():
    def predicate(ctx):
        return int(ctx.channel.id) == int(CTAM_CHNL[0])
    return commands.check(predicate)

def is_apt_chnl(ctx):
    return int(ctx.channel.id) == int(MOD_ACTION_CHNL[0])

def fun_pass():
    def predicate(ctx):
        return True if int(587085162416701440) in [int(i.id) for i in ctx.author.roles] else False
    return commands.check(predicate)

def is_JTexpo():
    def predicate(ctx):
        return 319199396724211722 == ctx.author.id
    return commands.check(predicate)
    
# // -- MAKING FLIE LOGS ON MACHINE -- //
def html_log(category = '', content = '',channel_name = '', channel_id = 0):
    mydir = "/home/jtexpo/html/{}/".format(category)
    ex = ""
    today = date.today()
    try:
        os.mkdir(mydir+str(today.year))
        print(mydir, str(today.year) ,  " Created ")
    except FileExistsError:
            print(mydir, str(today.year) ,  " already exists")
    #check month
    mydir = mydir+str(today.year)+"/"
    ex = ex + str(today.year)+"/"
    try:
        os.mkdir(mydir+str(today.month))
        print(mydir , str(today.month) ,  " Created ")
    except FileExistsError:
        print(mydir, str(today.month) ,  " already exists")
    #check day
    mydir = mydir+str(today.month)+"/"
    ex = ex + str(today.month)+"/"
    try:
        os.mkdir(mydir+str(today.day))
        print(mydir, str(today.day) ,  " Created ")
    except FileExistsError:
        print(mydir, str(today.day) ,  " already exists")
    mydir = mydir+str(today.day)+"/"
    ex = ex + str(today.day)+"/"
    file = open(mydir+"{}-{}.txt".format(channel_name,channel_id),"w")
    file.write(content)
    file.close()
    return ex

# // -- Loops -- //
async def Backup(bot):
    await bot.wait_until_ready()
    global ACTIVITY
    global DB_ACTIVITY
    global POINT
    global DB_POINT
    global RAFFLE
    global DB_RAFFLE
    global HIGHLIGHT_HIST
    while not bot.is_closed():
        conn = sqlite3.connect('Database.db')
        c = conn.cursor()

        c.execute("SELECT user_ID, message_count FROM activity_table;")
        DB_ACTIVITY = c.fetchall()
        c.execute("SELECT user_ID, points FROM point_table;")
        DB_POINT = c.fetchall()
        c.execute("SELECT user_ID FROM raffle_table;")
        DB_RAFFLE = c.fetchall()

        HIGHLIGHT_HIST = []

        await bot.get_channel(LOG[0]).send("Begining Backup : ```{}```".format(datetime.now()))
        # // -- Activity backup -- //
        for user in DB_ACTIVITY:
            if user[0] in ACTIVITY:
                c.execute("UPDATE activity_table SET message_count = {} WHERE user_ID = {}".format(ACTIVITY[user[0]]+user[1],user[0]))
        is_instance = False
        for user in ACTIVITY:
            for elm in DB_ACTIVITY:
                if user in elm:
                    is_instance = True
                    break
            if not is_instance:
                c.execute("INSERT INTO activity_table VALUES (NULL, {}, {});".format(user,ACTIVITY[user]))
            is_instance = False
        # // -- Point backup -- //
        for user in DB_POINT:
            if user[0] in POINT:
                c.execute("UPDATE point_table SET points = {} WHERE user_ID = {}".format(POINT[user[0]]+user[1],user[0]))
        is_instance = False
        for user in POINT:
            for elm in DB_POINT:
                if user in elm:
                    is_instance = True
                    break
            if not is_instance:
                c.execute("INSERT INTO point_table VALUES (NULL, {}, {});".format(user,POINT[user]))
            is_instance = False
        # // -- updating the raffle -- //
        for user in RAFFLE:
            c.execute("INSERT INTO raffle_table VALUES (NULL, {});".format(user))
        # // -- updating the count and the highscore -- //
        c.execute("UPDATE general_table SET info = '{}' WHERE title = 'CTAM-SCORE'".format(COUNT))
        c.execute("UPDATE general_table SET info = '{}' WHERE title = 'CTAM-HIGH-SCORE'".format(COUNT_HIGH))

        c.execute("SELECT user_ID, message_count FROM activity_table;")
        DB_ACTIVITY = c.fetchall()
        c.execute("SELECT user_ID, points FROM point_table;")
        DB_POINT = c.fetchall()
        c.execute("SELECT user_ID FROM raffle_table;")
        DB_RAFFLE = c.fetchall()

        conn.commit()
        conn.close()

        ACTIVITY = {}
        POINT = {}
        RAFFLE = []

        await bot.get_channel(LOG[0]).send("Backup Went Well : ```{}```".format(datetime.now()))
        # // -- repeat all of this once every 60 minuets -- //
        await asyncio.sleep(3600)

async def CheckForUpdate(bot):
    await bot.wait_until_ready()
    wlink  = 'http://explosm.net/'
    # // -- looking through the SQL databases to get all the channels to post in -- //
    conn = sqlite3.connect('Database.db')
    c = conn.cursor()
    c.execute("SELECT info FROM general_table WHERE title='COMIC-UPDATE';")
    chns = c.fetchall()
    c.execute("SELECT info FROM general_table WHERE title='LAST-COMIC';")
    com = c.fetchone()
    c.execute("SELECT info FROM general_table WHERE title='LAST-VIDEO';")
    vid = c.fetchone()
    conn.close()
    com = com[0]
    vid = vid[0]
    # // -- creating a list of channel objects -- //
    channels = []
    for chn in chns:
        channels.append(bot.get_channel(int(chn[0])))
    # // -- while the bot is online do -- //
    while not bot.is_closed():
         
        # // -- get the page source from 'http://explosm.net/' -- //
        try:
            await bot.get_channel(LOG[0]).send("Looking For Comic : ```{}```".format(datetime.now()))
            pageSource = str(urllib2.urlopen(wlink).read()).split()
        except Exception as error:
            await bot.get_channel(LOG[0]).send("AN ERROR OCCURED FINDING COMIC : ```{}```".format(error))
            await asyncio.sleep(300)
            continue
        try:

            # // -- check is there is a new comic -- //
            link = getComic(pageSource)
            if link != "NaN":
                # // -- if the database has the most up to date video do nothing -- //
                if link == com: 
                    await bot.get_channel(LOG[0]).send("```COMIC IS ALREADY UPDATED```")
                    await asyncio.sleep(300)
                    continue

                com = link
                # // -- if the comic is not the most up to date, update it then return the comic -- //
                conn = sqlite3.connect('Database.db')
                c = conn.cursor()
                c.execute("UPDATE general_table SET info = '{}' WHERE title='LAST-COMIC';".format(com))
                # // -- grabbing the author, avatar, and number -- //
                author,avatar,number = getComicInfo(pageSource)
                c.execute("UPDATE general_table SET info = '{}' WHERE title='COMIC-NUMBER';".format(number))
                conn.commit()
                conn.close()
                # // -- all the formating and creating of the embed -- //
                embdc = discord.Embed(title = "Comic Update!",
                        description = ("A comic created by **{}**!\nIf you like what you see checkout more on our website: [Explosm.net](http://explosm.net)\nAlso hop on our [discord](https://discord.gg/cyanide) if you're not already : [C&H_Official_Discord](https://discord.gg/cyanide)".format(author)),
                        colour = random.randint(0,0xffffff)
                        )
                embdc.set_thumbnail(url = str(avatar))
                embdc.set_image(url = 'http://'+str(link))
                embdc.set_footer(text = "Comic Number : {}".format(number))
                # // -- printing in all the channels the comic update -- //
                for chnl in channels:
                    update = await chnl.send(embed = embdc)
                    if chnl.is_news() == True:
                        await update.publish()
            # // -- check is there is a new video -- //
            link = getVideo(pageSource)
            if link != "NaN":
                # // -- if the database has the most up to date video do nothing -- //
                if link == vid: 
                    await bot.get_channel(LOG[0]).send("```VIDEO IS ALREADY UPDATED```")
                    await asyncio.sleep(300)
                    continue
                vid = link
                # // -- if the video is not the most up to date, update it then return the video -- //
                conn = sqlite3.connect('Database.db')
                c = conn.cursor()
                c.execute("UPDATE general_table SET info = '{}' WHERE title='LAST-VIDEO';".format(link))
                conn.commit()
                conn.close()
                # // -- all the formating and creating of the embed -- //
                embdv = discord.Embed(title = "Video Update!",
                        description = ("Guess what time it is? Time for you to watch our newest video! [Click Here For More!](http://explosm.net/)"),
                        colour = random.randint(0,0xffffff))
                embdv.set_image(url = "http://explosm.net/img/logo.png")
                # // -- printing in all the channels the comic update -- //
                for chnl in channels:
                    await chnl.send(embed = embdv)
                    update = await chnl.send(link)
                    if chnl.is_news() == True:
                        await update.publish()
            await bot.get_channel(LOG[0]).send("Comic Update Went Well : ```{}```".format(datetime.now()))
            # // -- repeat all of this once every 5 minuets -- //
            await asyncio.sleep(300)
        except Exception as error:
            await bot.get_channel(LOG[0]).send("AN ERROR OCCURED FINDING COMIC : ```{}```".format(error))
            continue

        

### STUFF FOR GETTING COMIC / VIDEO INFORMAION ###
# // -- Gets The Video From The Source Code -- //
def getVideo(src):
    # // -- For all the words in the souce -- //
    for i in src:
        # // -- If the phrase 'youtube.com/watch' is found -- //
        if 'youtube.com/watch' in i:
            # // -- creading a string and making it be the start of the href to the end of the string -- //
            p = i[i.index('"')+1:-1]
            # // -- returning the video -- //
            return p
    # // -- If there was no video link found in the source code -- //
    return "NaN"

# // -- Gets The Comic From The Source Code -- //
def getComic(src):
    # // -- For all the words in the souce -- //
    for i in src:
        # // -- If the phrase 'files.explosm.net/comics' is found -- //
        if "files.explosm.net/comics" in i:
            # // -- Some comics have a '?' and for some reason the imagine can't be pulled up if they do. This is mend to get around that weird cases -- //
            try:
                if '?' in i:
                    p = i[i.index('f'):i.index("?")]
                # // -- The comics that don't have the video the link can be found aswell, but because of unequal spaces that are in the source we have to trime the second " as such -- //
                else:
                    p = i[i.index('f'):i[i.index('"')+1:].index('"')+i.index('"')+1]
                # // -- Returning the comic -- //
                return p
            except:
                return "NaN"
    # // -- If there was no video link found in the source code -- //
    return "NaN"


# // -- A way to give the information on the comic -- //
def getComicInfo(src):
    sname = []
    name = 0
    author = "NaN"
    avatar = "NaN"
    number = "NaN"
    avaDic = {"202":"Matt Melvin","204":"Rob DenBleyker","206":"Kris Wilson","207":"Dave McElfatrick"}
    # // -- Originally this used to be much simpler and the comic picture would have the name; however, some comics started having others names such as a robbing containing 'rob' but written by dave. This is why this new was is inplace -- //
    # // -- For all the words in the souce -- //
    for i in src:
        # // -- If the phrase 'files.explosm.net/avatars' is found grab the pic they go by. This is in the event that any of the atrists change the pic -- //
        if 'files.explosm.net/avatars' in i:
            avatar = 'http:' + i[i.index('"')+1:i.index('jp')]+'jpg'
        # // -- grabbing the latest comic for the comic generator command, and updating it in the SQL database -- //
        if 'data-slug="comic' in i:
            number = i[i.index('c-')+2:-6]

    # // -- Getting all the values to return. Not returning inside the loop in the event something goes wrong : ie. a guest author -- //
    for i in avaDic:
        if i in avatar:
            author = avaDic[i]
    return author, avatar, number

### STUFF FOR LOGGING COMMANDS ###
# // -- Creating A Log of A Command Being Used -- //
async def log_command(bot,ctx,func_name):
    # // -- Creating and Embed -- //
    log_embed = discord.Embed(
        title = ('Robobert Command Log'),
        description = ("Command : {}\nContent : `{}`".format(func_name,ctx.message.content)),
        colour = random.randint(0,0xffffff)
        )
    # // -- Giving the Embed Fields -- //
    log_embed.add_field(name = "Guild", value = "{}".format(ctx.guild), inline = False)
    log_embed.add_field(name = "Channel", value = "{} : {}".format(ctx.channel,ctx.channel.id), inline = False)
    log_embed.add_field(name = "Author", value = "{} : {} : {}".format(ctx.author,ctx.author.nick,ctx.author.id), inline = False)
    log_embed.add_field(name = "Time", value = "{}".format(datetime.now()), inline = False)
    # // -- Sending the Embed -- //
    await bot.get_channel(LOG[0]).send(embed = log_embed)

# // -- A Function To Print Information In The Testing Server Error Chat -- //
async def error_log_command(bot,ctx,func_name,error):
    # // -- Creating and Embed -- //
    log_embed = discord.Embed(
        title = ('Robobert Error Log'),
        description = ("Command : {}\nContent : `{}`\nError : ```{}```".format(func_name,ctx.message.content,error)),
        colour = random.randint(0,0xffffff)
        )
    # // -- Giving the Embed Fields -- //
    log_embed.add_field(name = "Guild", value = "{}".format(ctx.guild), inline = False)
    log_embed.add_field(name = "Channel", value = "{} : {}".format(ctx.channel,ctx.channel.id), inline = False)
    log_embed.add_field(name = "Author", value = "{} : {} : {}".format(ctx.author,ctx.author.nick,ctx.author.id), inline = False)
    log_embed.add_field(name = "Time", value = "{}".format(datetime.now()), inline = False)
    # // -- Creating an Instance of a File and Setting it to the Thumbnail -- //
    # // -- Sending the Embed -- //
    await bot.get_channel(LOG[0]).send(embed = log_embed)
