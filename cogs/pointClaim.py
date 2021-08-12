from discord.ext import commands
import json, datetime
import discord
class claimPts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = json.load(open('pointsConf.json'))
    
    def changeBalance(self,amnt, user, method):
        with open("creds.json") as f:
            self.creds = json.load(f)
        if str(user.id) in self.creds.keys():

            if method == "+":
                self.creds[str(user.id)] += amnt
            else:
                self.creds[str(user.id)] -= amnt
            with open("creds.json", "w") as f:
                json.dump(self.creds, f)
        else:
            if method == "+":
                self.creds[str(user.id)] = amnt
            else:
                self.creds[str(user.id)] = amnt
    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        self.changeBalance(self.config['daily'],ctx.author, '+')
        await ctx.send("Daily claimed! You now have {:.2f} points.".format(self.creds[str(ctx.author.id)]))
    @daily.error
    async def command_name_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"Slow it down bro!",description=f"Try again in {error.retry_after:.2f}s.", color=0xF00000)
            await ctx.send(embed=em)
    @commands.command()
    @commands.cooldown(1, 604800, commands.BucketType.user)
    async def weekly(self, ctx):
        self.changeBalance(self.config['weekly'],ctx.author, '+')
        await ctx.send("Weekly claimed! You now have {:.2f} points.".format(self.creds[str(ctx.author.id)]))
    @weekly.error
    async def command_name_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"Slow it down bro!",description=f"Try again in {error.retry_after:.2f}s.", color=0xF00000)
            await ctx.send(embed=em)
    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def hourly(self, ctx):
        self.changeBalance(self.config['hourly'],ctx.author, '+')
        await ctx.send("Hourly claimed! You now have {:.2f} points.".format(self.creds[str(ctx.author.id)]))
    @hourly.error
    async def command_name_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"Slow it down bro!",description=f"Try again in {error.retry_after:.2f}s.", color=0xF00000)
            await ctx.send(embed=em)
def setup(bot):
    bot.add_cog(claimPts(bot))