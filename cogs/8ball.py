from discord.ext import commands
import random, discord
class eightball(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["8ball"])
    async def eightball(self, ctx):
        if len(ctx.message.content.split()) == 1:
            return await ctx.send('Please ask a question.')
        answerList = [	"It is certain",
						"It is decidedly so",
						"Without a doubt",
						"Yes, definitely",
						"You may rely on it",
						"As I see it, yes",
						"Most likely",
						"Outlook good",
						"Yes",
						"Signs point to yes",
						"Reply hazy try again",
						"Ask again later",
						"Better not tell you now",
						"Cannot predict now",
						"Concentrate and ask again",
						"Don't count on it",
						"My reply is no",
						"My sources say no",
						"Outlook not so good",
						"Very doubtful"]
        msg = '{}'.format(random.choice(answerList))
        embed = discord.Embed(title="", colour=random.randint(0, 0xFFFFFF), description=f"{msg}")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @eightball.error
    async def command_name_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"Slow it down bro!",description=f"Try again in {error.retry_after:.2f}s.", color=0xF00000)
            await ctx.send(embed=em)
def setup(bot):
	bot.add_cog(eightball(bot))