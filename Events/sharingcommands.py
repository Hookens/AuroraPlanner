# Copyright (C) 2025 Hookens
# See the LICENSE file in the project root for details.

from discord import SlashCommandOptionType, default_permissions, SlashCommandGroup
from discord.bot import Bot
from discord.commands import Option
from discord.commands.context import ApplicationContext
from discord.ext import commands

from Debug.debughelpers import try_func_async
from Utilities.constants import EventTexts

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Events.sharingmethods import SharingMethods

class SharingCommands(commands.Cog):
    schedule = SlashCommandGroup("schedule", EventTexts.S_SCHEDULE)

    def __init__(self, bot: Bot):
        self.bot = bot

    @schedule.command(name="share", description=EventTexts.C_COPY)
    @default_permissions(manage_messages=True,)
    @try_func_async()
    async def slash_share(self, ctx: ApplicationContext,
                               messageid: Option(str, EventTexts.F_MESSAGE, required=True),
                               servers: Option(str, EventTexts.F_SERVERS, min_length=1, max_length=256, required=True),
                               channel: Option(SlashCommandOptionType.channel, EventTexts.F_DIFFCHANNEL, required=False)):

        await ctx.interaction.response.defer(ephemeral=True)

        methods: SharingMethods = self.bot.get_cog("SharingMethods")
        if methods is not None:
            await ctx.interaction.followup.send(embed=await methods.share_event(ctx, int(messageid), servers, channel))

def setup(bot):
    bot.add_cog(SharingCommands(bot))