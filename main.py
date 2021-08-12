from discord.ext import commands
from discord.ext.commands import BucketType
import discord
from datetime import datetime
TOKEN = "ODYyNjc1MTcwNjM5NzQwOTI4.YOby3A.oK_qyr5sIIeU19P0LIL-UlSXXMs"
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

cogs_to_load = ["cogs.botOnline",
                "cogs.coinflip",
                "cogs.crashCmd",
                "cogs.transfer",
                "cogs.checkPoints",
                "cogs.dice",
                "cogs.giveCredsAdmin",
                "cogs.helpCog",
                "cogs.rain",
                "cogs.8ball",
                "cogs.giveCreditsOnJoin",
                "cogs.udCommand",
                "cogs.roulette",
                "cogs.StakeMines",
                "cogs.handleListing",
                "cogs.pointClaim"
                ]
time_last_sent = datetime.utcnow()
@bot.event
async def on_message(message):

    await bot.process_commands(message)


if __name__ == "__main__":
    for extension in cogs_to_load:
        try:
            print("loaded", extension)
            bot.load_extension(extension)
        except Exception as e:
            print(e)
    
bot.run(TOKEN)