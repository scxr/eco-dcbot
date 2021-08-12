import discord, json
from discord.ext import commands

class Handles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def add_handle(self, ctx, *, args=None):
        """Adds a handle to the list of handles."""
        if ctx.message.author.guild_permissions.administrator:
            if args is None:
                await ctx.send("Invalid arguments. Please use `!add_handle <type> <handle> <bin>`")
                return

            arguments = args.split(" ")
            try:
                _type = arguments[0]
                _type = _type[0].upper() + _type[1:].lower()
                handle = arguments[1]
                _bin = arguments[2]
            except ValueError:
                await ctx.send("Invalid arguments. Please use `!add_handle <type> <handle> <bin>`")
                return
            with open("handles.json", "r") as f:
                handles = json.load(f)
            info = {"handle_name":handle, "bin":_bin, "co":"0", "offerer":""}
            handles[_type].append(info)
            with open("handles.json", "w") as f:
                json.dump(handles, f)
            await ctx.send("Handle added.")
            with open("handlesConf.json", "r") as f:
                conf = json.load(f)
            if conf[_type] != "":
                id_ = conf[_type]["message"]
                chan = self.bot.get_channel(conf[_type]["chan"])
                embedM = await chan.fetch_message(int(id_))
                with open("handles.json", "r") as f:
                    handles = json.load(f)
                body = ''
                for values in handles[_type]:
                    try:
                        offerer = await self.bot.fetch_user(int(values["offerer"]))
                    except Exception as e:
                        print(e)
                        offerer = "NA"
                    body += f'**@{values["handle_name"]}** - `BIN : ${values["bin"]} - C/O: {values["co"]}` by {offerer.mention if offerer!="NA" else "NA"}\n'
                    print(body, values)
                embed = discord.Embed(title=f"{_type} Handles", description=body)
                await embedM.edit(embed=embed)
        else:
            await ctx.send("You don't have permission to use this command.")
            return
    
    @commands.command()
    async def remove_handle(self, ctx, *, args=None):
        """Removes a handle from the list of handles."""
        if ctx.message.author.guild_permissions.administrator:
            if args is None:
                await ctx.send("Invalid arguments. Please use `!remove_handle <type> <handle>`")
                return

            arguments = args.split(" ")
            try:
                _type = arguments[0]
                _type = _type[0].upper() + _type[1:].lower()
                handle = arguments[1]
            except ValueError:
                await ctx.send("Invalid arguments. Please use `!remove_handle <type> <handle>`")
                return
            with open("handles.json", "r") as f:
                handles = json.load(f)
            for i in handles[_type]:
                if i["handle_name"] == handle:
                    handles[_type].remove(i)
            with open("handles.json", "w") as f:
                json.dump(handles, f)
            await ctx.send("Handle removed.")
            with open("handlesConf.json", "r") as f:
                conf = json.load(f)
            if conf[_type] != {}:
                id_ = conf[_type]["message"]
                chan = self.bot.get_channel(conf[_type]["chan"])
                embedM = await chan.fetch_message(int(id_))
                with open("handles.json", "r") as f:
                    handles = json.load(f)
                body = ''
                for values in handles[_type]:
                    try:
                        offerer = await self.bot.fetch_user(int(values["offerer"]))
                    except Exception as e:
                        print(e)
                        offerer = "NA"
                    body += f'**@{values["handle_name"]}** - `BIN : ${values["bin"]} - C/O: {values["co"]}` by {offerer.mention if offerer!="NA" else "NA"}\n'
                    print(body, values)
                embed = discord.Embed(title=f"{_type} Handles", description=body)
                await embedM.edit(embed=embed)

        else:
            await ctx.send("You don't have permission to use this command.")
            return
    
    @commands.command()
    async def list_handles(self, ctx, *, args=None):
        """Lists all handles."""
        if ctx.message.author.guild_permissions.administrator:
            if args is None:
                await ctx.send("Invalid arguments. Please use `!list_handles <type>`")
            try:
                _type = args.split(" ")[0]
                _type = _type[0].upper() + _type[1:].lower()
            except ValueError:
                await ctx.send("Invalid arguments. Please use `!list_handles <type>`")
            embed = discord.Embed(title=f"{_type} Handles")
            with open("handles.json", "r") as f:
                handles = json.load(f)
            body = ''
            for values in handles[_type]:
                try:
                    offerer = await self.bot.fetch_user(int(values["offerer"]))
                except Exception as e:
                    print(e)
                    offerer = "NA"
                body += f'**@{values["handle_name"]}** - `BIN : ${values["bin"]} - C/O: {values["co"]}` by {offerer.mention if offerer!="NA" else "NA"}\n'
                print(body, values)
            embed = discord.Embed(title=f"{_type} Handles", description=body)
            m = await ctx.send(embed=embed)
            with open("handlesConf.json", "r") as f:
                handles = json.load(f)
            handles[_type] = {"chan":ctx.channel.id,"message":m.id}
            with open("handlesConf.json", "w") as f:
                json.dump(handles, f)
    
    @commands.command()
    async def offer(self, ctx, *, args=None):
        """Offers a handle to the bot."""
        if args is None:
            await ctx.send("Invalid arguments. Please use `!offer <platform> <handle> <offer>`")
            return
        arguments = args.split(" ")
        try:
            platform = arguments[0]
            platform = platform[0].upper() + platform[1:].lower()
            handle = arguments[1]
            offer = float(arguments[2])

        except ValueError:
            await ctx.send("Invalid arguments. Please use `!offer <platform> <handle> <offer>`")
            return
        except IndexError:
            await ctx.send("Invalid arguments. Please use `!offer <platform> <handle> <offer>`")
            return
        with open("handles.json", "r") as f:
            handles = json.load(f)
        cnt = 0
        successfulOffer = False
        for i in handles[platform]:

            if i["handle_name"] == handle:
                if float(i["co"]) < offer:
                    await ctx.send("Your offer has been submitted.")
                    handles[platform][cnt]["co"] = str(offer)
                    handles[platform][cnt]["offerer"] = ctx.author.id
                    successfulOffer = True
                    with open("handles.json", "w") as f:
                        json.dump(handles, f)
                    
                else:
                    await ctx.send("Your offer is lower than the current CO")
                    return
            cnt += 1
        if not successfulOffer:
            
            return
        with open("handlesConf.json", "r") as f:
            handles = json.load(f)
        with open("handlesConf.json", "r") as f:
            conf = json.load(f)
        id_ = handles[platform]['message']
        chan = self.bot.get_channel(conf[platform]["chan"])
        embedM = await chan.fetch_message(int(id_))
        with open("handles.json", "r") as f:
            handles = json.load(f)
        body = ''
        for values in handles[platform]:
            try:
                offerer = await self.bot.fetch_user(int(values["offerer"]))
            except Exception as e:
                print(e)
                offerer = "NA"
            body += f'**@{values["handle_name"]}** - `BIN : ${values["bin"]} - C/O: {values["co"]}` by {offerer.mention if offerer!="NA" else "NA"}\n'
            print(body, values)
        embed = discord.Embed(title=f"{platform} Handles", description=body)
        await embedM.edit(embed=embed)

def setup(bot):
    bot.add_cog(Handles(bot))