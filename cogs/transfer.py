from discord.ext import commands
import discord, json
class TransferPoints(commands.Cog):
    """Transfer points to another user"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["tpoints", "transfer"])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def transferPoints(self, ctx, user: discord.Member, points: int):
        """Transfer points to another user"""
        if ctx.author.id == user.id:
            await ctx.send("You can't give yourself points!")
            return
        if points < 0:
            await ctx.send("You can't give negative points!")
            return
        with open("creds.json") as f:
            creds = json.load(f)
        if str(user.id) not in creds.keys():
            await ctx.send("You can't give points to someone not in our database")
            return
        else:
            if creds[str(ctx.author.id)] < points:
                await ctx.send("You don't have enough points to give!")
                return
            creds[str(ctx.author.id)] -= points
            creds[str(user.id)] += points
            with open("creds.json", "w") as f:
                json.dump(creds, f)
            await ctx.send("You gave {} points to {}".format(points, user.mention))
            return
    @transferPoints.error
    async def command_name_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"Slow it down bro!",description=f"Try again in {error.retry_after:.2f}s.", color=0xF00000)
            await ctx.send(embed=em)
def setup(bot):
    bot.add_cog(TransferPoints(bot))