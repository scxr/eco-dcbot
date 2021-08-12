from discord.ext import commands

import discord, random


class BlackJack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def blackjack(self, ctx, *, args=None):
        """
        BlackJack discord command
        """
        if args is None:
            await ctx.send("The syntax for this command is : `!blackjack bet_amount`")
            return
        try:
            amount_bet = int(args.split()[0])
        except:
            await ctx.send(f"`{args.split()[0]}` is not a valid bet amount")
            return
        
        cards = {
            "2":"<:2_:868847288326426634>",
            "3":"<:3_:868847288200593418>",
            "4":"<:4_:868847288330629170>",
            "5":"<:5_:868847288288673872>",
            "6":"<:6_:868847288032833537>",
            "7":"<:7_:868847287886049361>",
            "8":"<:8_:868847288120922182>",
            "9":"<:9_:868847288083152956>",
            "10":"<:10:868847287709868043>",
            "jack":"<:jack:868847289790251039>",
            "queen":"<:queen:868847290117414912>",
            "king":"<:king:868847289861546074>",
            "ace":"<:ace:868847286531260477>"
            }
        values = {
            "jack":10,
            "queen":10,
            "king":10,
            "ace":1
        }
        choice = random.choice(list(cards.keys()))
        try:
            choice = int(choice)
        except:
            choice = values[choice]
        cardsU = []
        curr_card_values = 0
        for i in range(2):
            cardsU.append(random.choice(list(cards.keys())))
        for i in cardsU:
            try:
                val = int(i)
            except:
                val = values[i]
            curr_card_values += val
        

def setup(bot):
    bot.add_cog(BlackJack(bot))