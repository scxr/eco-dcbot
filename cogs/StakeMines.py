from discord.ext import commands
import discord
import random
import asyncio
import json
class Mines(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    def changeBalance(self,amnt, user, method):
        with open("creds.json") as f:
            self.creds = json.load(f)
        if method == "+":
            self.creds[str(user.id)] += amnt
        else:
            self.creds[str(user.id)] -= amnt
        with open("creds.json", "w") as f:
            json.dump(self.creds, f)
    @commands.command()
    async def mines(self, ctx, *, args=None):
        if args is None:
            await ctx.send("Please re-check how to run this command, the format is !mines amount_of_mines bet_amount")
            return

        try:
            arg_split = args.split()
            amount_mines = int(arg_split[0])
            amount_bet = int(arg_split[1])
        except:
            await ctx.send("Please re-check how to run this command, the format is !mines amount_of_mines bet_amount")
            return
        
        if amount_mines < 1 or amount_bet < 1:
            await ctx.send("You cannot have less than 1 for mine or balance")
            return
        if amount_mines > 24:
            await ctx.send("You cannot have more than 24 for mine")
            return
        with open("creds.json") as f:
            self.creds = json.load(f)
        if amount_bet > self.creds[str(ctx.author.id)]:
            await ctx.send("You don't have enough credits to roll that many dice.")
            return

        setup = [[":heart:", ":blue_heart:", ":orange_heart:", ":purple_heart:", ":two_hearts:"],
                [":blush:", ":wink:", ":angry:", ":thinking:",":hugging:"],
                [":pig:", ":wolf:", ":horse:", ":snail:", ":penguin:"], 
                [":green_apple:", ":pear:", ":peach:", ":coconut:", ":avocado:"], 
                [":basketball:", ":football:", ":8ball:", ":rugby_football:",":yo_yo:"]]
        real_emotes = {
            "❤️":":heart:",
            "💙":":blue_heart:",
            "🧡": ":orange_heart:",
            "💜":":purple_heart:",
            "💕":":two_hearts:",
            "😊":":blush:",
            "😉":":wink:",
            "😠":":angry:",
            "🤔":":thinking:",
            "🤗":":hugging:",
            "🐷":":pig:",
            "🐺":":wolf:",
            "🐴":":horse:", 
            "🐌":":snail:",
            "🐧":":penguin:",
            "🍏":":green_apple:",
            "🍐":":pear:",
            "🍑":":peach:",
            "🥥":":coconut:",
            "🥑":":avocado:",
            "🏀":":basketball:",
            "🏈":":football:",
            "🎱":":8ball:", 
            "🏉":":rugby_football:",
            "🪀":":yo_yo:",
            "❌":":x:"
        }
        with open("stakeMines.json") as f:
            stakeMines = json.load(f)
        mine_places = [random.randint(0,25) for i in range(amount_mines)]
        correct_amnt = 0
        cant_have = [setup[m//5 if m//5 != 5 else 4][(m%5)-1 if m%5 != 0 else 0] for m in mine_places]
        print(cant_have, mine_places)
        embed = discord.Embed(title="mines", description="\n".join(" ".join(x) for x in setup), colour=random.randint(0x00, 0xFFFFFF))
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text="to mine do : `!mine emote` *you have 5 seconds*")
        m = await ctx.send(embed=embed)
        def check(message):
            return message.author == ctx.author
        while True:
            try:
                msg = await self.bot.wait_for('message', check=check, timeout=10)
                
                if msg.content not in real_emotes.keys():
                    await ctx.send("Not a valid emote!")
                    continue
                else:
                    emote_name = real_emotes[msg.content]
                    if msg.content == "❌":
                        print("oof")
                        type_of_end = "Success"
                        break
                    
                     
                    if emote_name in cant_have:
                        type_of_end = "Fail"
                        break
                    else:
                        correct_amnt += 1
                    setup = [[_el if _el != emote_name else ":coin:" for _el in _ar] for _ar in setup]
                    print(setup)
                    embed = discord.Embed(title="mines", description="\n".join(" ".join(x) for x in setup), colour=random.randint(0x00, 0xFFFFFF))
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                    key = f"m{amount_mines}d{correct_amnt}"
                    multiplier = stakeMines[key]
                    embed.add_field(name="Multiplier", value=multiplier)
                    embed.set_footer(text="to mine do : `!mine emote` *you have 10 seconds*\nTo stop send :x:")
                    await m.edit(embed=embed)
                    await msg.delete()
            except asyncio.TimeoutError:
                await ctx.send("You took too long to respond")
                type_of_end = "Success"
                break
        final = []
        for i in setup:
            tmp = []
            for j in i:
                tmp.append(":coin:" if j not in cant_have else ":x:")
            final.append(tmp)
        if type_of_end == "Success":
            value = "{:.2f}".format((int(amount_bet) * float(multiplier)) - int(amount_bet))
            self.changeBalance(ctx.author.id, value, "+")
        else:
            self.changeBalance(ctx.author.id, amount_bet, "-")
        embed = discord.Embed(title=f"mines - {type_of_end}", description="\n".join(" ".join(x) for x in final), colour=random.randint(0x00, 0xFFFFFF))
        embed.add_field(name="You won" if type_of_end == "Success" else "You lost", value=f"{value} points" if type_of_end == "Success" else f"{amount_bet} points")
        embed.set_footer(text=f"Your multiplier was : {multiplier}")
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await m.edit(embed=embed)
def setup(bot):
    bot.add_cog(Mines(bot))