# Copyright (C) 2025 Hookens
# See the LICENSE file in the project root for details.

from discord import SlashCommandOptionType, TextChannel, default_permissions, SlashCommandGroup
from discord.bot import Bot
from discord.commands import Option
from discord.commands.context import ApplicationContext
from discord.ext import commands
from discord.role import Role

from Debug.debughelpers import try_func_async

class EventCommands(commands.Cog):
    schedule = SlashCommandGroup("schedule", "Event related commands")

    def __init__(self, bot: Bot):
        self.bot = bot

    @schedule.command(name="add", description="Schedule a new event.")
    @default_permissions(manage_messages=True,)
    @try_func_async()
    async def slash_schedule(self, ctx: ApplicationContext,
                                   title: Option(str, "The title of the event.", min_length=1, max_length=256, required=True),
                                   description: Option(str, "The description of the event.", max_length=4096, required=True),
                                   time: Option(str, "The date and time of the event, in 'DD-MM-YYYY HH:mm' format, on UTC.", required=True),
                                   modpacktitle: Option(str, "The title of the modpack.", max_length=254, required=False),
                                   modpacklink: Option(str, "The link to the modpack.", max_length=766, required=False),
                                   minimumattendance: Option(int, "The minimum attendance for the event.", min_value=1, max_value=100, required=False),
                                   ping: Option(Role, "Role to ping with the event.", required=False),
                                   channel: Option(SlashCommandOptionType.channel, "A different channel in which to post the event.", required=False),
                                   requireddlc: Option(str, "The required DLC for the event.", max_length=1024, required=False),
                                   additionaldetails: Option(str, "The additional details (gear/year/team composition/etc) for the event.", max_length=1024, required=False),
                                   imagelink: Option(str, "The image preview of the event.", max_length=1024, required=False)):
        
        await ctx.interaction.response.defer(ephemeral=True)

        methods = self.bot.get_cog("EventMethods")
        if methods is not None:
            await ctx.interaction.followup.send(embed=await methods.handle_event(ctx, 0, title, description, time, modpacktitle, modpacklink, minimumattendance, requireddlc, additionaldetails, imagelink, channel, ping))

    @schedule.command(name="edit", description="Edit a previously scheduled event in the current channel.")
    @default_permissions(manage_messages=True,)
    @try_func_async()
    async def slash_edit(self, ctx: ApplicationContext,
                               messageid: Option(str, "The id of the event (message) to edit.", required=True),
                               title: Option(str, "The title of the event.", min_length=1, max_length=256, required=False),
                               description: Option(str, "The description of the event.", max_length=4096, required=False),
                               time: Option(str, "The date and time of the event, in 'DD-MM-YYYY HH:mm' format, on UTC.", required=False),
                               modpacktitle: Option(str, "The title of the modpack.", max_length=254, required=False),
                               modpacklink: Option(str, "The link to the modpack.", max_length=766, required=False),
                               channel: Option(SlashCommandOptionType.channel, "The different channel in which the event is.", required=False),
                               requireddlc: Option(str, "The required DLC for the event.", max_length=1024, required=False),
                               minimumattendance: Option(int, "The minimum attendance for the event.", min_value=1, max_value=100, required=False),
                               additionaldetails: Option(str, "The additional details (gear/year/team composition/etc) for the event.", max_length=1024, required=False),
                               imagelink: Option(str, "The image preview of the event.", max_length=1024, required=False)):

        await ctx.interaction.response.defer(ephemeral=True)

        methods = self.bot.get_cog("EventMethods")
        if methods is not None:
            await ctx.interaction.followup.send(embed=await methods.handle_event(ctx, int(messageid), title, description, time, modpacktitle, modpacklink, minimumattendance, requireddlc, additionaldetails, imagelink, channel))

    @schedule.command(name="copy", description="Copy a previously scheduled event into its original command form.")
    @default_permissions(manage_messages=True,)
    @try_func_async()
    async def slash_edit(self, ctx: ApplicationContext,
                               messageid: Option(str, "The id of the event (message) to copy.", required=True),
                               channel: Option(SlashCommandOptionType.channel, "The different channel in which the event is.", required=False)):

        await ctx.interaction.response.defer(ephemeral=True)

        methods = self.bot.get_cog("EventMethods")
        if methods is not None:
            await ctx.interaction.followup.send(embed=await methods.copy_event(ctx, int(messageid), channel))

def setup(bot):
    bot.add_cog(EventCommands(bot))