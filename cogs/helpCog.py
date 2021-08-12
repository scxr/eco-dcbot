from discord.ext import commands
import random, discord
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')
    
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def help(self, ctx):
        embed = discord.Embed(title="Help", description="This is a list of commands you can use.", color=random.randint(0x000000, 0xFFFFFF))
        embed.add_field(name="!help", value="Shows this message.", inline=False)
        embed.add_field(name="!crash", value="Play a game of crash with the bot\nSyntax : `!crash amountToBet`\nEg : `!crash 100`", inline=False)
        embed.add_field(name="!coinflip", value="Flip a coin\nSyntax : `!coinflip amount heads or tails`\nEg: `!coinflip 100 heads`", inline=False)
        embed.add_field(name="!roll", value="Roll a dice\nSyntax : `!roll bet_amount number youre rolling`\nEg: `!roll 100 50`", inline=False)
        embed.add_field(name="!8ball", value="Ask 8ball a question")
        embed.add_field(name="!mines", value="Play a game of mines\nSyntax : `!mines bet_amount number of mines`\nEg: `!mines 100 23`", inline=False)
        embed.add_field(name="!transfer", value="Send money to a user\nSyntax: `!transfer @user amount`",inline=False)
        #mbed.add_field(name="!list_handles", value="List all handles for a platform, usage : `!list_handles platform` (REQUIRES ADMIN)\nEg : `!list_handles twitch`", inline=False)
        #mbed.add_field(name="!offer", value="Make an offer for a handle, usage : `!offer platform handle offer`", inline=False)
        #mbed.add_field(name="!add_handle", value="Add a handle to list, usage : `!add_handle platform handle bin` (REQUIRES ADMIN)\nEg : `!add_handle twitch myHandle 1000`", inline=False)
        #mbed.add_field(name="!remove_handle", value="Remove a handle from list, usage : `!remove_handle platform handle` (REQUIRES ADMIN)\nEg : `!remove_handle twitch myHandle`", inline=False)
        embed.add_field(name="!hourly", value="Collect hourly points\nUsage: `!hourly`", inline=False)
        embed.add_field(name="!daily", value="Collect daily points\nUsage: `!daily`", inline=False)
        embed.add_field(name="!weekly", value="Collect weekly points\nUsage: `!weekly`", inline=False)
        embed.set_footer(text="Written by nemo#0043")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @help.error
    async def command_name_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"Slow it down bro!",description=f"Try again in {error.retry_after:.2f}s.", color=0xF00000)
            await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Help(bot))