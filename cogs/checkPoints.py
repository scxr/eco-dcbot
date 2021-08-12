from discord.ext import commands
import discord, json, random
class GetPoints(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def points(self, ctx, user: discord.Member=None):
        if user is None:
            user = ctx.author
        with open("creds.json", "r") as f:
            creds = json.load(f)
        if str(user.id) in creds.keys():
            pass
        else:
            await ctx.send("This user has no points.")
            return
        creds = "{:.2f}".format(creds[str(user.id)])
        embed = discord.Embed(title=f"Point count", description=f"This user has {creds} points", colour=random.randint(0x000000, 0xFFFFFF))
        if user:
            embed.set_author(name=user.name, icon_url=user.avatar_url)
        else:
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @points.error
    async def command_name_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"Slow it down bro!",description=f"Try again in {error.retry_after:.2f}s.", color=0xF00000)
            await ctx.send(embed=em)
def setup(bot):
    bot.add_cog(GetPoints(bot))