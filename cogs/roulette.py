from discord.ext import commands
import random, discord, json
class Roulette(commands.Cog):
    """Roulette game"""
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
    async def roulette(self, ctx, *, arg=None):
        """Play a game of roulette"""
        try:
            args = arg.split()
            amnt = float(args[1])
            if args[0].lower() not in ["bronze", "gold", "silver"]:
                return await ctx.send("Please re check the help command to see how to run this command")
            else:
                choice = args[0].lower()
        except:
            
            return await ctx.send("Please re check the help command to see how to run this command")

        setup = ["gold", "silver","silver","silver","silver","silver","silver","silver", "bronze","bronze","bronze","bronze","bronze","bronze","bronze"]
        our_choice = random.choice(setup)
        embed = discord.Embed(title="Roulette!", colour=random.randint(0x00, 0xFFFFFF))
        if our_choice == choice:
            embed = discord.Embed(title="Roulette!", colour=random.randint(0x00, 0xFFFFFF))
            if our_choice == "gold":
                won = amnt * 13
                embed.add_field(name="You Win!", value=":coin: You won {}$!".format(amnt * 13))
            elif our_choice == "silver" or our_choice == "bronze":
                won = amnt * 1
                embed.add_field(name="You Win!", value=":coin: You won {}$!".format(amnt * 1))
            self.changeBalance(won, ctx.author, "+")
        else:
            
            embed.add_field(name="You lost :(", value=f":x: You chose {choice} but we landed on {our_choice}")

        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Roulette(bot))