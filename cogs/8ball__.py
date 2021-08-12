import asyncio
import discord
import random
from   discord.ext import commands



class EightBall(commands.Cog):

	# Init with the bot reference, and a reference to the settings var
	def __init__(self, bot):
		self.bot = bot

	@commands.command(hidden=True)
	async def lmap(self, ctx, *, question = None):

		await ctx.invoke(self.eightball,question=question)

	@commands.command(aliases=["8ball"])
	async def eightball(self, ctx, *, question = None):
		"""Get some answers."""
		if question == None:
		    msg = 'You need to ask me a question first.'
		
        	return await ctx.channel.send(msg)
			

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
						"Very doubtful"	]
		randnum = random.randint(0, len(answerList)-1)
		msg = '{}'.format(answerList[randnum])
        embed = discord.embed(title="8ball", colour=random.randint(0, 0xFFFFFF), description=msg)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
		# Say message
def setup(bot):
	# Add the bot
	bot.add_cog(EightBall(bot))