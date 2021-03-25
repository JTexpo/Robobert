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

class SQL(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(name = 'SQL_Manual')
    @Util.is_JTexpo()
    async def SQL_Manual(self,ctx):
        # // -- Log The Commands Use -- //
        await Util.log_command(self.bot,ctx,"SQL_Manual :")

        def check_message(message):
            return ((message.author == ctx.author) and (message.channel == ctx.channel))

        conn = sqlite3.connect('Database.db')
        c = conn.cursor()
        c_embed = discord.Embed(title = "Please Write Out The SQL Command, Be Careful",
                description = "This command is only useable by JTexpo",
                colour = random.randint(0,0xffffff)
                )
        await ctx.send(embed = c_embed)
        in_msg = await self.bot.wait_for('message', timeout=60.0, check = check_message)
        c.execute(in_msg.content)
        conn.commit()
        conn.close()
        c_embed = discord.Embed(title = "Everything Went Well Sucessfully",
                description = "You Wrote : `{}`".format(in_msg.content),
                colour = random.randint(0,0xffffff)
                )
        await ctx.send(embed = c_embed)



    @commands.command(name = 'show_server_database_table_contents',
                      aliases = ['show_server_db_table_contents','ssdbtc'])
    @Util.is_JTexpo()
    async def show_server_database_table_contents(self,ctx):
        # // -- Log The Commands Use -- //
        await Util.log_command(self.bot,ctx,"show_server_database_table_contents")
        color = random.randint(0,0xffffff)
        def check_message(message):
            return ((message.author == ctx.author) and (message.channel == ctx.channel))
        
        try:
            conn = sqlite3.connect('Database.db')
            c = conn.cursor()
            c.execute("""SELECT name FROM sqlite_master
                    WHERE type='table'
                    ORDER BY name;""")
            my_tables = c.fetchall()
            index = 1
            table_dict = {}
            c_msg = ''
            sql_c_msg = ''
            for table in my_tables:
                table_dict[index] = table[0]
                c_msg += "{} : {}\n".format(index,table[0])
                index += 1
            c_embed = discord.Embed(title = "Please Select The Number Of The Table You Wish To See",
                description = c_msg,
                colour = color
                )
            await ctx.send(embed = c_embed)
    
            in_msg = await self.bot.wait_for('message', timeout=60.0, check = check_message)
            c.execute("SELECT * FROM {}".format(table_dict[int(in_msg.content)]))
            # // -- Getting the contents of the table -- //
            contents = c.fetchall()
            # // -- getting how many rows there are -- //
            total_rows = len(contents)
            # // -- getting how mayn elements there are --//
            total_elements = len(contents[0])
            # // -- making a list of 0, to then figure out the longest char for table formating -- //
            longest_char_list = [0]*total_elements
            # // -- itterating through the elemens of each row, row is the changing varible -- //
            for e in range(total_elements):
                for r in range(total_rows):
                    longest_char_list[e] = len(str(contents[r][e])) if len(str(contents[r][e])) > longest_char_list[e] else longest_char_list[e]
            # // -- creating a message to print the table -- //
            c_msg = ''
            for row in contents:
                index = 0
                for element in row:
                    # // -- dividing the message into parts -- //
                    if (index != 0) : c_msg += ' | '
                    c_msg += "{}".format(element).ljust(longest_char_list[index])
                    index += 1
                c_msg += "\n"
            # // -- Confirmation Embed -- //
            expire = 10
            while len(c_msg) > 1800 and expire > 0:
                c_embed = discord.Embed(title = "SQL Table Of {}".format(table_dict[int(in_msg.content)]),
                        description = "```"+c_msg[:1800]+"```",
                        colour = color
                        )
                c_msg = c_msg[1800:]
                await ctx.send(embed = c_embed)
                expire -= 1
            c_embed = discord.Embed(title = "SQL Table Of {}".format(table_dict[int(in_msg.content)]),
                    description = "```"+c_msg[:1800]+"```",
                    colour = color
                    )
        except Exception as error:
            # // -- Log The Commands Use -- //
            await Util.error_log_command(self.bot,ctx,"show_server_database_table_contents",error)
        await ctx.send(embed = c_embed)
        return

    
    @commands.command(name = 'update_server_database_table',
                      aliases = ['update_server_db_table','usdbt'])
    @Util.is_JTexpo()
    async def update_server_database_table(self,ctx):
        # // -- Log The Commands Use -- //
        await Util.log_command(self.bot,ctx,"update_server_database_table")
        color = random.randint(0,0xffffff)

        def check_message(message):
            return ((message.author == ctx.author) and (message.channel == ctx.channel))
        
        try:
            conn = sqlite3.connect('Database.db')
            c = conn.cursor()
            c.execute("""SELECT name FROM sqlite_master
                    WHERE type='table'
                    ORDER BY name;""")
            my_tables = c.fetchall()
            index = 1
            table_dict = {}
            c_msg = ''
            sql_c_msg = 'UPDATE '
            for table in my_tables:
                table_dict[index] = table[0]
                c_msg += "{} : {}\n".format(index,table[0])
                index += 1
            c_embed = discord.Embed(title = "Please Select The Number Of The Table You Wish To Add To",
                description = c_msg,
                colour = color
                )
            await ctx.send(embed = c_embed)
            
            in_msg = await self.bot.wait_for('message', timeout=60.0, check = check_message)
            c.execute("SELECT * FROM {}".format(table_dict[int(in_msg.content)]))
            current = c.fetchall()
            sql_c_msg += " {} SET ".format(table_dict[int(in_msg.content)])
            c.execute("PRAGMA table_info({});".format(table_dict[int(in_msg.content)]))
            collumns = c.fetchall()
            c_embed = discord.Embed(title = "Please Type The Database ID You Want To Update",
                colour = color
                )
            c_out_msg = await ctx.send(embed = c_embed)
            
            in_msg = await self.bot.wait_for('message', timeout=60.0, check = check_message)
            sql_c_msg_end_part = ' WHERE db_ID = {};'.format(in_msg.content)
            index = 0
            elm = int(in_msg.content)-1
            for collumn in collumns:                
                if collumn[1] == 'db_ID':
                    continue
                
                if index != 0:
                    sql_c_msg += ','
                index += 1
                
                c_embed = discord.Embed(title = "Please Type The {}".format(collumn[1]),
                    description = "\n---\nCurrently : {}".format(current[elm][index]),
                    colour = color
                    )
                await c_out_msg.edit(embed = c_embed)
                in_msg = await self.bot.wait_for('message', timeout=60.0, check = check_message)
                if "VARCHAR" in collumn[2]:
                    sql_c_msg += ' {} = "{}" '.format(collumn[1], in_msg.content)
                else : sql_c_msg += ' {} = {} '.format(collumn[1], in_msg.content)
            sql_c_msg += sql_c_msg_end_part
            c.execute(sql_c_msg)
            conn.commit()
            conn.close()
            c_embed = discord.Embed(title = "Everything Went Well Sucessfully",
                description = "You Wrote : `{}`".format(sql_c_msg),
                colour = color
                )
            
        except Exception as error:
            # // -- Log The Commands Use -- //
            await Util.error_log_command(self.bot,ctx,"update_server_database_table",error)
        await ctx.send(embed = c_embed)
        return


def setup(bot):
    bot.add_cog(SQL(bot))