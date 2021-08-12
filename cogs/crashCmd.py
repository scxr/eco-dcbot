from discord.ext import commands
import discord
import random, hmac, time, hashlib, asyncio, decimal, json
class Crash(commands.Cog):
    """
    We use the same math as roobet, not as cryptographically secure as we generate random hashes
    but otherwise would have to track the games, without supercomputers this is practically
    impossible to guess the result.
    """
    def __init__(self, bot):
        self.bot = bot
        self.salt = "0000000000000000000fa3b65e43e4240d71762a5bf397d5304b2596d116859c"

    def changeBalance(self,amnt, user, method):
        with open("creds.json") as f:
            self.creds = json.load(f)
        if method == "+":
            self.creds[str(user.id)] += amnt
        else:
            self.creds[str(user.id)] -= amnt
        with open("creds.json", "w") as f:
            json.dump(self.creds, f)
    def drange(self, x, y, jump):
        while x < y:
            yield float(x)
            x += decimal.Decimal(jump)
    def getCrash(self):
        "we use the current time as our seed. to change the seed to smth else, change the following:str.encode(str(time.time()))"
        hash ="%032x" % random.getrandbits(256)

        hm = hmac.new(str.encode(hash), str.encode(str(time.time())), hashlib.sha256)
        hm.update(self.salt.encode("utf-8"))
        h = hm.hexdigest()
        if (int(h, 16) % 33 == 0):
            return 1
        h = int(h[:13], 16)
        e = 2**52
        x= (((100 * e - h) / (e-h)) // 1) / 100.0
        return float("{:.2f}".format(x))
    
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def crash(self, ctx, *, msg):
        colour = random.randint(0, 0xffffff)
        try:
            amnt = int(msg.split()[0])
        except:
            await ctx.send("Please enter an amnt to bet")
            return
        crashLimit = self.getCrash()
        print(crashLimit)
        with open("creds.json") as f:
            self.creds = json.load(f)
        if amnt > self.creds[str(ctx.author.id)]:
            await ctx.send("You don't have enough to bet that much")
            return
        embed = discord.Embed(title="CRASH GAME!")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Crash", value="React with 🔴 to cashout", inline=False)
        embed.add_field(name="Multiplier", value="1.0", inline=True)
        embed.add_field(name="Value", value=str(amnt), inline=True)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🔴")
        def check(reaction, user):
            return reaction.message.id == msg.id and user.id == ctx.author.id and str(reaction.emoji) == "🔴"
        toadd = 0
        for i in list(self.drange(1, 100, '0.1')):
            re = False
            cache_msg = discord.utils.get(self.bot.cached_messages, id=msg.id)
            for r in cache_msg.reactions:
                users = await r.users().flatten()
                if ctx.author in users:
                    re = True
            if re:
                successCrash = discord.Embed(title="CRASH GAME!")
                successCrash.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                m = "{:.1f}x".format(i-0.1)
                successCrash.add_field(name="Crash", value=f"We cashed out at {m}", inline=False)
                
                successCrash.add_field(name="Multiplier", value=m, inline=True)
                
                successCrash.add_field(name="Value", value=str(value), inline=True)
                self.changeBalance(toadd, ctx.author, "+")
                await msg.edit(embed=successCrash)
                return
            profit = amnt * i
            toadd = (amnt * i) - amnt
            if i > crashLimit:
                crashEmbed = discord.Embed(title="CRASH GAME!")
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                crashEmbed.add_field(name="Crash", value=f"We crashed at {i}x", inline=False)
                
                crashEmbed.add_field(name="Multiplier", value=f"{i}x", inline=True)
                crashEmbed.add_field(name="Value", value="CRASHED", inline=True)
                self.changeBalance(amnt, ctx.author, "-")
                await msg.edit(embed=crashEmbed)
                return
            newembed = discord.Embed(title="CRASH GAME!")
            newembed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            newembed.add_field(name="Crash", value="React with 🔴 to cashout", inline=False)
            newembed.add_field(name="Multiplier", value=f"{i}x", inline=True)
            value = "{:.2f}".format(profit)
            newembed.add_field(name="Value", value=str(value)+" pts", inline=True)
            await msg.edit(embed=newembed)


            


            await asyncio.sleep(0.5)

    @crash.error
    async def command_name_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"Slow it down bro!",description=f"Try again in {error.retry_after:.2f}s.", color=0xF00000)
            await ctx.send(embed=em)
def setup(bot):
    bot.add_cog(Crash(bot))