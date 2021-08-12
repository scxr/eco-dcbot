from discord.ext import commands
import random, json, discord
class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dice_lim = 100
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
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def roll(self, ctx, *, args):
        try:

            amnt = float(args.split()[0])
            number = int(args.split()[1])
        except Exception:
            await ctx.send("Invalid syntax.\n`!roll amount number`")
            return
        with open("creds.json") as f:
            self.creds = json.load(f)
        if amnt > self.creds[str(ctx.author.id)]:
            await ctx.send("You don't have enough credits to roll that many dice.")
            return
        if number > 99:
            await ctx.send("That's too high. Max (99)")
            return
        rolled = random.randint(0, self.dice_lim)
        if number < rolled:
            e = discord.Embed(title="Dice game", description=f"You lost! The dice rolled a `{rolled}` and you bet to roll under `{number}`.",colour=0x00F000)
            e.add_field(name="Win chance", value=f'{number}%')
            e.set_author(name=ctx.author,icon_url=ctx.author.avatar_url)
            e.set_footer(text="eco bot")
            await ctx.send(embed=e)
            self.changeBalance(amnt, ctx.author, "-")
        else:
            profit = amnt + (amnt * (1-number/100))
            e = discord.Embed(title="Dice game", description=f"You won! The dice rolled a `{rolled}` and you bet to roll under `{number}`.\nYou have gained `{profit}` points.",colour=0x00F000)
            e.add_field(name="Win chance", value=f'{number}%')
            e.set_author(name=ctx.author,icon_url=ctx.author.avatar_url)
            e.set_footer(text="eco bot")
            await ctx.send(embed=e)
            self.changeBalance(amnt+profit, ctx.author, "+")
    @roll.error
    async def command_name_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"Slow it down bro!",description=f"Try again in {error.retry_after:.2f}s.", color=0xF00000)
            await ctx.send(embed=em)
def setup(bot):
    bot.add_cog(Dice(bot))