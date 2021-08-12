from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import json
import discord
class GivePtsAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    @commands.has_role("Bot Admin")
    async def givepts(self, ctx, user: discord.Member, amount: int):
        """Give a user points."""
        if amount < 0:
            await ctx.send("Cannot give negative points, maybe you meant to use `rmvpts`?")
            return
        with open("creds.json") as f:
            creds = json.load(f)
        if str(user.id) not in creds.keys():
            creds[str(user.id)] = amount
        else:
            creds[str(user.id)] += amount
        with open("creds.json", "w") as f:
            json.dump(creds, f)
        await ctx.send("{} has been given {} pts.".format(user.mention, amount))
    
    @givepts.error
    async def givepts_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
            await ctx.send(text)
    
    @commands.command(pass_context=True)
    @commands.has_role("Bot Admin")
    async def rmvpts(self, ctx, user: discord.Member, amount: int):
        """Give a user points."""
        if amount < 0:
            await ctx.send("Cannot give negative points, maybe you meant to use `rmvpts`?")
            return
        with open("creds.json") as f:
            creds = json.load(f)
        if str(user.id) not in creds.keys():
            creds[str(user.id)] = 0
        else:
            creds[str(user.id)] -= amount
        with open("creds.json", "w") as f:
            json.dump(creds, f)
        await ctx.send("{} has had {} pts removed.".format(user.mention, amount))

def setup(bot):
    bot.add_cog(GivePtsAdmin(bot))