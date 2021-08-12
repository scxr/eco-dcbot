from discord.ext import commands
import random
import discord
import asyncio
import json
class coinflip(commands.Cog):
    """Flip a coin"""

    def __init__(self, bot):
        self.bot = bot

    def changeBalance(self,amnt, user, method):
        with open("creds.json") as f:
            self.creds = json.load(f)
        if method == "+":
            self.creds[str(user.id)] += amnt
        else:
            self.creds[str(user.id)] -= amnt
        with open("creds.json", "w") as f:
            json.dump(self.creds, f)
    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def coinflip(self, ctx, *, msg):
        """Flip a coin"""
        msg = msg.split()
        try:
            selection = msg[1]
            amnt = int(msg[0])
            if selection.lower() == "heads" or selection.lower() == "tails":
                pass
            else:
                await ctx.send("Please re-check the command format")
                return
        except:
            await ctx.send("Please re-check the command format")
            return
        with open("creds.json") as f:
            self.creds = json.load(f)
        if amnt > self.creds[str(ctx.author.id)]:
            await ctx.send("You don't have enough credits to roll that many dice.")
            return
        author = ctx.message.author
        msg = discord.Embed(colour=0xdaa520, description= "")
        msg.title = ""
        msg.add_field(name=":floppy_disk: Coin Flip", value="Flipping a coin...")
        await ctx.send(embed=msg)
        await asyncio.sleep(2)
        
        msg = discord.Embed(colour=0xdaa520, description= "")
        msg.title = ""
        if random.randint(0, 1) == 0:
            if selection.lower() != "heads":
                emote = "cry"
                self.changeBalance(int(amnt), author, "-")
            else:
                emote = "tada"
                self.changeBalance(int(amnt), author, "+")

            msg.add_field(name=f":{emote}: Coin Flip", value="You flipped a **Heads**!")
        else:
            if selection.lower() != "tails":
                emote = "cry"
                self.changeBalance(int(amnt), author, "-")
            else:
                emote = "tada"
                self.changeBalance(int(amnt), author, "+")
            msg.add_field(name=f":{emote}: Coin Flip", value="You flipped a **Tails**!")
        await ctx.send(embed=msg)

def setup(bot):
    bot.add_cog(coinflip(bot))