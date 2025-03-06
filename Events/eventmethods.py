# Copyright (C) 2025 Hookens
# See the LICENSE file in the project root for details.

from datetime import datetime
from discord import ApplicationContext, Message, TextChannel
from discord.bot import Bot
from discord.ext import commands
from discord.embeds import Embed
from discord.role import Role

from Debug.debughelpers import try_func_async
from Events.eventview import EventView

class EventMethods(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    def get_time_field(self, time: datetime) -> str:
        timestr: str = f"<t:{int(time.timestamp())}:F> - Lobby open 30 minutes prior"
        
        return f"{timestr}\n:clock2: <t:{int(time.timestamp())}:R>"

    def format_description(self, description: str)-> str:
        return description.replace("\\n", "\n")

    @try_func_async()
    async def handle_event(self, ctx: ApplicationContext, embedid: int, title: str = None, description: str = None, time: str = None, modpacktitle: str = None, modpacklink: str = None, minimumattendance: int = None, requireddlc: str = None, additionaldetails: str = None, imagelink: str = None, channel: TextChannel = None, ping: Role = None):
        embeds = self.bot.get_cog("Embeds")
        embed: Embed = Embed()
        embed.colour = 0x8663FC
        message: Message = None
        action: str = "creat"

        if embedid != 0:
            action = "edit"

            try:
                if channel is not None:
                    message = await channel.fetch_message(embedid)
                else:
                        message = await ctx.channel.fetch_message(embedid)
            except Exception:
                pass

            if message is None or not (message.author.id == self.bot.user.id and any(message.embeds[0].fields)):
                return await embeds.generate_embed("Event edition error", f"No event with the provided ID was found{ ' in the given channel' if channel is not None else ''}.", 0xCC0000)
            
            embed = message.embeds[0]

        if title is not None:
            embed.title = title
        
        if description is not None:
            embed.description = self.format_description(description)

        if time is not None:
            try:
                stime: str = self.get_time_field(datetime.strptime(time, "%d-%m-%Y %H:%M"))
            except:
                stime = "Error parsing time input, refer to option tooltip."
            
            if message is not None:
                embed.set_field_at(index=0, name="Time", value=stime, inline=False)
            else:
                embed.add_field(name="Time", value=stime, inline=False)

        if imagelink is not None:
            embed.set_image(url=imagelink)

        if message is not None:
            if modpacktitle is not None:
                value: str = embed.fields[1].value
                packlink: str = value.split("]")[1]
                embed.set_field_at(index=1, name="Modpack", value=f"[{modpacktitle}]{packlink}", inline=False)

            if modpacklink is not None:
                value: str = embed.fields[1].value
                packname: str = value.split("(")[0]
                embed.set_field_at(index=1, name="Modpack", value=f"{packname}({modpacklink})", inline=False)

            if minimumattendance is not None:
                embed.set_field_at(index=2, name="Minimum Attendance", value=f"{minimumattendance}", inline=False)

            if requireddlc is not None:
                embed.set_field_at(index=3, name="Required DLC", value=requireddlc, inline=False)

            if additionaldetails is not None:
                embed.set_field_at(index=4, name="Additional Details", value=self.format_description(additionaldetails), inline=False)
                
            await message.edit(embed=embed)
        else:
            modpack = f"[{modpacktitle}]({modpacklink})" if modpacklink is not None else "-"
            embed.add_field(name="Modpack", value=modpack, inline=False)
            embed.add_field(name="Minimum Attendance", value=minimumattendance or "-", inline=False)
            embed.add_field(name="Required DLC", value=requireddlc or "-", inline=False)
            embed.add_field(name="Additional Details", value=self.format_description(additionaldetails or "-"), inline=False)
            embed.add_field(name=":white_check_mark: Accepted", value=f"-", inline=True)
            embed.add_field(name=":no_entry_sign: Declined", value=f"-", inline=True)
            embed.add_field(name=":grey_question: Tentative", value=f"-", inline=True)

            if channel is None:
                message: Message = await ctx.channel.send(content="" if ping is None else ping.mention, embed=embed, view=EventView())
            else:
                message: Message = await channel.send(content="" if ping is None else ping.mention, embed=embed, view=EventView())

            await message.edit(embed=message.embeds[0].set_footer(text=f"Event ID: {message.id}"))

        return await embeds.generate_embed(f"Event {action}ion success", f"The event was successfully {action}ed.", 0x00AA00)

    @try_func_async()
    async def copy_event(self, ctx: ApplicationContext, embedid: int, channel: TextChannel = None):
        embeds = self.bot.get_cog("Embeds")
        message: Message = None

        try:
            if channel is not None:
                message = await channel.fetch_message(embedid)
            else:
                    message = await ctx.channel.fetch_message(embedid)
        except Exception:
            pass

        if message is None or not (message.author.id == self.bot.user.id and any(message.embeds[0].fields)):
            return await embeds.generate_embed("Event edition error", f"No event with the provided ID was found{ ' in the given channel' if channel is not None else ''}.", 0xCC0000)
        
        embed = message.embeds[0]

        embed_description = embed.description.replace('\n', '\\n')

        hastime = embed.fields[0].value.count(":F>") > 0
        if hastime:
            time: datetime = datetime.fromtimestamp(int(embed.fields[0].value.split(":F>")[0].replace("<t:", "")))
            timestr = time.strftime("%d-%m-%Y %H:%M")
            
        haspack = embed.fields[1].value != "-"
        if haspack:
            modpack = embed.fields[1].value.split("](")
            modpacktitle = modpack[0].replace('[', '')
            modpacklink = modpack[1].replace(')', '')

        hasattendance = embed.fields[2].value != "-"
        hasrequireddlc = embed.fields[3].value != "-"

        hasadditionaldetails = embed.fields[4].value != "-"
        if hasadditionaldetails :
            embed_additionaldetails = embed.fields[4].value.replace('\n', '\\n')

        hasimage = len(embed.image.url) > 0

        description = ("```"
                     +  "\n/schedule add"
                     + f"\ntitle:{embed.title}"
                     + f"\ndescription:{embed_description}"
                     + (f"\ntime:{timestr}" if hastime else "")
                     + (f"\nmodpacktitle:{modpacktitle}" if haspack else "")
                     + (f"\nmodpacklink:{modpacklink}" if haspack else "")
                     + (f"\nminimumattendance:{embed.fields[2].value}" if hasattendance else "")
                     + (f"\nrequireddlc:{embed.fields[3].value}" if hasrequireddlc else "")
                     + (f"\nadditionaldetails:{embed_additionaldetails}" if hasadditionaldetails else "")
                     + (f"\nimagelink:{embed.image.url}" if hasimage else "")
                     +  "```")
        
        return await embeds.generate_embed(f"Creation command for {embed.title}", description, 0x00AA00)
            

def setup(bot):
    bot.add_cog(EventMethods(bot))