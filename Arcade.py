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

class Arcade(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        conn = sqlite3.connect('Database.db')
        c = conn.cursor()
        c.execute("SELECT word FROM hangman_table;")
        self.word_tuple = c.fetchall()
        c.execute("SELECT role_ID FROM role_table WHERE title='EXECUTIONER';")
        self.executioner = c.fetchone()
        c.execute("SELECT role_ID FROM role_table WHERE title='CCA';")
        self.cca = c.fetchone()
        c.execute("SELECT role_ID FROM role_table WHERE title='LIZARD';")
        self.lizard = c.fetchone()
        c.execute("SELECT role_ID FROM role_table WHERE title='ONE-IN-ONEHUNDRED';")
        self.onehundred = c.fetchone()
        conn.close()

    @commands.command(name = "guess")
    @Util.is_arcade_chnl()
    async def guess(self,ctx, number = 100):
        await Util.log_command(self.bot,ctx,"guess")
        def check_message(message):
            return ((message.author == ctx.author) and (message.channel == ctx.channel))
        color = random.randint(0,0xffffff)
        answer = random.randint(1,number)
        def build_embed(string,guesses):
            embed = discord.Embed(
                title = "{}'s game of Guess".format(ctx.author),
                description = ("I'm thinking of a number bewteen 1 and {}\n{}".format(number,string)),
                colour = color)
            embed.set_footer(text = "Type 'end' to end the game : You've Guessed {} Times".format(guesses))
            return embed
        guesses = 0
        game_str = "**__Please Just Type A Number__**"
        game_msg = await ctx.send(embed = build_embed(game_str,guesses))
        while True:
            in_msg = await self.bot.wait_for('message', timeout=120.0, check = check_message)
            await in_msg.delete()
            if 'end' in in_msg.content.lower():
                await ctx.send("quiting game...")
                return
            try:
                if int(in_msg.content) > answer:
                    game_str = 'Close, but the number is : **Lower Than {}!**'.format(in_msg.content)
                elif int(in_msg.content) < answer:
                    game_str = 'Close, but the number is : **Higher Than {}!**'.format(in_msg.content)
                else:
                    if ((guesses == 0) and (number == 100)):
                        await ctx.author.add_roles(ctx.guild.get_role(self.onehundred[0]))
                    game_str = 'Congrats! **{}** was the number!'.format(answer)
                    await game_msg.edit(embed = build_embed(game_str,guesses+1))
                    await ctx.send("You Win!")
                    return
                guesses += 1
            except Exception as error:
                game_str = "**__Please Just Type A Number__**"
            await game_msg.edit(embed = build_embed(game_str,guesses))

    @commands.command(name = "hangman")
    @Util.is_arcade_chnl()
    async def hangman(self,ctx):
        await Util.log_command(self.bot,ctx,"hangman")
        def check_message(message):
            return ((message.author == ctx.author) and (message.channel == ctx.channel))
        color = random.randint(0,0xffffff)
        word_num = random.randint(0,len(self.word_tuple)-1)
        word = list(self.word_tuple[word_num][0])
        for i in range(len(word)):
            if word[i] != ' ':
                word[i] = '_'
        guess_log = []
        strike = 0
        hang_s = ["```.┌───────┐",
                ".┃       ",
                ".┃       ",
                ".┃     ",
                ".┃       ",
                ".┃      ",
                "/-\\```"]
        strike_s = ["",
                "┋",
                "0",
                "/ | \\",
                "|",
                "/ \\"]
        def build_embed():
            embed = discord.Embed(
                title = "{}'s game of Hangman".format(ctx.author),
                description = ("I'm thinking of a word that goes something like this :\n"+
                            '```'+' '.join(word)+'```\n'+'\n'.join(hang_s)+'\n\n Guesses :\n'+
                            ' '.join(guess_log)
                            ),
                colour = color)
            embed.set_footer(text = "Type 'end' to end the game")
            return embed
        game_msg = await ctx.send(embed = build_embed())
        while True:
            in_msg = await self.bot.wait_for('message', timeout=120.0, check = check_message)
            await in_msg.delete()
            if 'end' in in_msg.content.lower():
                await ctx.send("quiting game...")
                return
            if len(in_msg.content) > 1:
                await ctx.send("{} Make Sure To Only Type 1 Letter, Or 'END' To end".format(ctx.author.mention))
                continue
            elif in_msg.content in guess_log:
                continue
            guess_log.append(in_msg.content.lower())
            if in_msg.content.lower() in self.word_tuple[word_num][0].lower():
                word = list(self.word_tuple[word_num][0])
                for i in range(len(word)):
                    if (word[i] == ' ') or (word[i].lower() in guess_log):
                        continue
                    word[i] = '_'
            else:
                strike += 1
                hang_s[strike] += strike_s[strike]
            await game_msg.edit(embed = build_embed())
            if strike == 5:
                await ctx.send("Game Over, The Word Was : {}".format(self.word_tuple[word_num]))
                return
            if str(''.join(word)) == str(self.word_tuple[word_num][0]):
                if strike == 0:
                    await ctx.author.add_roles(ctx.guild.get_role(self.executioner[0]))
                await ctx.send("You Win!")
                return

    @commands.command(name = "rock_paper_scissors",
                        aliases = ["rps"])
    @Util.is_arcade_chnl()
    async def rock_paper_scissors(self,ctx):
        await Util.log_command(self.bot,ctx,"rock_paper_scissors")

        def check_reaction(reaction,user):
            return ((user == ctx.author) and
            ((reaction.emoji == "\U0000270A") or (reaction.emoji == "\U0000270B") or (reaction.emoji == "\U0000270C")))

        color = random.randint(0,0xffffff)
        embed = discord.Embed(title = "Rock Paper Scissors Shoot!",
                    description = "{} React Either Rock Paper Or Scissors, Then I'll Reveal My Hand\n{} : ? v ? : Robobert".format(ctx.author.mention,ctx.author.name),
                    colour = color
                    )
        rps_message = await ctx.send(embed = embed)
        await rps_message.add_reaction("\U0000270A")
        await rps_message.add_reaction("\U0000270B")
        await rps_message.add_reaction("\U0000270C")

        reaction, user = await self.bot.wait_for('reaction_add',check = check_reaction,timeout = 60)
        guess = random.randint(0,2)
        if guess == 0:
            e_guess = "\U0000270A"
        elif guess == 1:
            e_guess = "\U0000270B"
        else:
            e_guess = "\U0000270C"

        if reaction.emoji == e_guess:
            embed = discord.Embed(title = "Rock Paper Scissors Shoot!",
                        description = "{} : {} v {} : Robobert\n***DRAW!***".format(
                                ctx.author.mention,reaction.emoji,e_guess),
                        colour = color
                        )
        elif (((reaction.emoji == "\U0000270A") and (guess == 1)) or
              ((reaction.emoji == "\U0000270B") and (guess == 2)) or
              ((reaction.emoji == "\U0000270C") and (guess == 0))):
            embed = discord.Embed(title = "Rock Paper Scissors Shoot!",
                        description = "{} : {} v {} : Robobert\n***You Lose!***".format(
                                ctx.author.mention,reaction.emoji,e_guess),
                        colour = color
                        )
        else:
            await ctx.author.add_roles(ctx.guild.get_role(self.lizard[0]))
            embed = discord.Embed(title = "Rock Paper Scissors Shoot!",
                        description = "{} : {} v {} : Robobert\n***You Win!***".format(
                                ctx.author.mention,reaction.emoji,e_guess),
                        colour = color
                        )
        await rps_message.edit(embed = embed)

    @commands.command(name = "tick_tac_toe",
                        aliases = ["ttt"])
    @Util.is_arcade_chnl()
    async def tick_tac_toe(self,ctx):
        await Util.log_command(self.bot,ctx,"tick_tac_toe")
        def check_message(message):
            return ((message.author == ctx.author) and (message.channel == ctx.channel))
        board = ['1','2','3',
                '4','5','6',
                '7','8','9']
        color = random.randint(0,0xffffff)
        def has_won():
            if   ((board[0] == board[1]) and (board[0] == board[2])) : return board[0]
            elif ((board[3] == board[4]) and (board[3] == board[5])) : return board[3]
            elif ((board[6] == board[7]) and (board[6] == board[8])) : return board[6]
            elif ((board[0] == board[3]) and (board[0] == board[6])) : return board[0]
            elif ((board[1] == board[4]) and (board[1] == board[7])) : return board[1]
            elif ((board[2] == board[5]) and (board[2] == board[8])) : return board[2]
            elif ((board[0] == board[4]) and (board[0] == board[8])) : return board[0]
            elif ((board[2] == board[4]) and (board[2] == board[6])) : return board[2]
            elif not(('1' == board[0])or('2' == board[1])or('3' == board[2])or
                    ('4' == board[3])or('5' == board[4])or('6' == board[5])or
                    ('7' == board[6])or('8' == board[7])or('9' == board[8])): return 'tie'
            else : return ' '
        def build_embed():
            embed = discord.Embed(title = "{}'s' Game of Tick Tac Toe".format(ctx.author),
                description = "{} is X's and Robobert is O's``` {} | {} | {}\n-----------\n {} | {} | {}\n-----------\n {} | {} | {}```".format(
                    ctx.author.mention,board[0],board[1],board[2],board[3],board[4],board[5],board[6],board[7],board[8]),
                    colour = color
                    )
            embed.set_footer(text = "Type 'end' to end the game")
            return embed
        turn = random.randint(0,1)
        game_msg = await ctx.send(embed = build_embed())
        while True:
            if has_won() != ' ':
                break
            await game_msg.edit(embed = build_embed())
            if turn == 1:
                while True:
                    ai_move = random.randint(0,8)
                    if (board[ai_move] != 'X') and (board[ai_move] != 'O'):
                        board[ai_move] = 'O'
                        turn = 0
                        break
            if has_won() != ' ':
                break
            await game_msg.edit(embed = build_embed())
            if turn == 0:
                while True:
                    in_msg = await self.bot.wait_for('message', timeout=120.0, check = check_message)
                    await in_msg.delete()
                    if 'end' in in_msg.content.lower():
                        await ctx.send("quiting game...")
                        return
                    try:
                        if (board[int(in_msg.content)-1] != 'X') and (board[int(in_msg.content)-1] != 'O'):
                            board[int(in_msg.content)-1] = 'X'
                            turn = 1
                            break
                    except:
                        await ctx.send("{} please send a number or ")
        await game_msg.edit(embed = build_embed())
        if has_won() == 'tie':
            await ctx.send("Game Over! It's a ***TIE***")
        if has_won() == 'O':
            await ctx.send("Game Over! ***You LOSE***")
        if has_won() == 'X':
            await ctx.author.add_roles(ctx.guild.get_role(self.cca[0]))
            await ctx.send("Game Over! ***You WIN***")




def setup(bot):
    bot.add_cog(Arcade(bot))
