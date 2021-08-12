from discord.ext import commands
import discord, random, requests
class UrbanDict(commands.Cog):
    """Urban Dictionary lookup"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def define(self, ctx, *, word):
        """Define a word"""
        word = word.lower()
        url = "http://api.urbandictionary.com/v0/define?term={}".format(word)
        resp = requests.get(url)
        data = resp.json()
        if data["list"]:
            definition = data["list"][0]["definition"]
            example = data["list"][0]["example"]
            embed = discord.Embed(title="Define a word", colour=random.randint(0, 0xFFFFFF))
            embed.add_field(name="Definition", value=definition, inline=True)
            embed.add_field(name="Example", value=example, inline=True)
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

        else:
            await ctx.send("**{}** not found".format(word))

def setup(bot):
    bot.add_cog(UrbanDict(bot))
