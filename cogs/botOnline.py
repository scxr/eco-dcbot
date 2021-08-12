from discord.ext import commands

class Online(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot Online! Logged in as : ", self.bot.user)

def setup(bot):
    bot.add_cog(Online(bot))