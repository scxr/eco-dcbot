from discord.ext import commands
import random, json, discord
class Rain(commands.Cog):
    """Rain is a cog for the bot to make it rain."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def rain(self, ctx):
        channel = ctx.channel
        lastAuthors = []
        with open("creds.json") as f:
            data = json.load(f)
        try:
            if data[str(ctx.author.id)] < 350:
                await ctx.send("You must have at least 350 pts to make it rain") 
        except:
            pass
        async for msg in channel.history(limit=200):
            if msg.author not in lastAuthors and msg.author != ctx.author:
                lastAuthors.append(msg.author)
            if len(lastAuthors) == 10:
                break
        msg = [author.mention for author in lastAuthors]
        amnt = random.randint(100,350)
        each_person = amnt/len(lastAuthors)
        await channel.send(f"Made it rain {amnt} points " + ', '.join(msg))
        data[str(ctx.author.id)] -= amnt
        for person in lastAuthors:
            if str(person.id) in data.keys():
            
                data[str(person.id)] += each_person
            else:
                data[str(person.id)] = each_person
        with open("creds.json", "w") as f:
            json.dump(data, f)


    @rain.error
    async def command_name_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"Slow it down bro!",description=f"Try again in {error.retry_after:.2f}s.", color=0xF00000)
            await ctx.send(embed=em)
def setup(bot):
    bot.add_cog(Rain(bot))