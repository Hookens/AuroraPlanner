# Copyright (C) 2025 Hookens
# See the LICENSE file in the project root for details.

from discord import SlashCommandOptionType, default_permissions, SlashCommandGroup
from discord.bot import Bot
from discord.commands import Option
from discord.commands.context import ApplicationContext
from discord.ext import commands
from discord.role import Role

from Debug.debughelpers import try_func_async
from Utilities.constants import EventTexts

class EventCommands(commands.Cog):
    schedule = SlashCommandGroup("schedule", EventTexts.S_SCHEDULE)

    def __init__(self, bot: Bot):
        self.bot = bot

    @schedule.command(name="add", description=EventTexts.C_ADD)
    @default_permissions(manage_messages=True,)
    @try_func_async()
    async def slash_schedule(self, ctx: ApplicationContext,
                                   title: Option(str, EventTexts.F_TITLE, min_length=1, max_length=256, required=True),
                                   description: Option(str, EventTexts.F_DESC, max_length=4096, required=True),
                                   time: Option(str, EventTexts.F_TIME, required=True),
                                   modpacktitle: Option(str, EventTexts.F_MODTITLE, max_length=254, required=False),
                                   modpacklink: Option(str, EventTexts.F_MODLINK, max_length=766, required=False),
                                   minimumattendance: Option(int, EventTexts.F_ATTENDANCE, min_value=1, max_value=100, required=False),
                                   ping: Option(Role, EventTexts.F_PING, required=False),
                                   channel: Option(SlashCommandOptionType.channel, EventTexts.F_CHANNEL, required=False),
                                   requireddlc: Option(str, EventTexts.F_DLC, max_length=1024, required=False),
                                   additionaldetails: Option(str, EventTexts.F_DETAILS, max_length=1024, required=False),
                                   imagelink: Option(str, EventTexts.F_IMAGE, max_length=1024, required=False)):
        
        await ctx.interaction.response.defer(ephemeral=True)

        methods = self.bot.get_cog("EventMethods")
        if methods is not None:
            await ctx.interaction.followup.send(embed=await methods.handle_event(ctx, 0, title, description, time, modpacktitle, modpacklink, minimumattendance, requireddlc, additionaldetails, imagelink, channel, ping))

    @schedule.command(name="edit", description=EventTexts.C_EDIT)
    @default_permissions(manage_messages=True,)
    @try_func_async()
    async def slash_edit(self, ctx: ApplicationContext,
                               messageid: Option(str, EventTexts.F_MESSAGE, required=True),
                               title: Option(str, EventTexts.F_TITLE, min_length=1, max_length=256, required=False),
                               description: Option(str, EventTexts.F_DESC, max_length=4096, required=False),
                               time: Option(str, EventTexts.F_TIME, required=False),
                               modpacktitle: Option(str, EventTexts.F_MODTITLE, max_length=254, required=False),
                               modpacklink: Option(str, EventTexts.F_MODLINK, max_length=766, required=False),
                               channel: Option(SlashCommandOptionType.channel, EventTexts.F_DIFFCHANNEL, required=False),
                               requireddlc: Option(str, EventTexts.F_DLC, max_length=1024, required=False),
                               minimumattendance: Option(int, EventTexts.F_ATTENDANCE, min_value=1, max_value=100, required=False),
                               additionaldetails: Option(str, EventTexts.F_DETAILS, max_length=1024, required=False),
                               imagelink: Option(str, EventTexts.F_IMAGE, max_length=1024, required=False)):

        await ctx.interaction.response.defer(ephemeral=True)

        methods = self.bot.get_cog("EventMethods")
        if methods is not None:
            await ctx.interaction.followup.send(embed=await methods.handle_event(ctx, int(messageid), title, description, time, modpacktitle, modpacklink, minimumattendance, requireddlc, additionaldetails, imagelink, channel))

    @schedule.command(name="copy", description=EventTexts.C_COPY)
    @default_permissions(manage_messages=True,)
    @try_func_async()
    async def slash_edit(self, ctx: ApplicationContext,
                               messageid: Option(str, EventTexts.F_MESSAGE, required=True),
                               channel: Option(SlashCommandOptionType.channel, EventTexts.F_DIFFCHANNEL, required=False)):

        await ctx.interaction.response.defer(ephemeral=True)

        methods = self.bot.get_cog("EventMethods")
        if methods is not None:
            await ctx.interaction.followup.send(embed=await methods.copy_event(ctx, int(messageid), channel))

def setup(bot):
    bot.add_cog(EventCommands(bot))