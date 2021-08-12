from discord.ext import commands
import json
class coinsOnJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open("creds.json", "r") as f:
            creds = json.load(f)
        if member.id in creds.keys():
            print("Already given this person 10 credits before")
        else:
            creds[member.id] = 10
            with open("creds.json", "w") as f:
                json.dump(creds, f)
            print("New user joined, giving them 10 credits")
            await member.send_message("You have been given 10 points for joining the server")
            await member.send_message("You can use `!points` to check your balance")
def setup(bot):
    bot.add_cog(coinsOnJoin(bot))