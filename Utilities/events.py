# Copyright (C) 2025 Hookens
# See the LICENSE file in the project root for details.

from discord.activity import Activity
from discord.bot import Bot
from discord.enums import ActivityType
from discord.ext import commands

from Debug.debughelpers import try_func_async
from Utilities.constants import LoggingDefaults

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Debug.logging import Logging

class Events(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    @try_func_async()
    async def on_ready (self):
        logging: Logging = self.bot.get_cog("Logging")
        if not logging: return
        
        await logging.log_event(f"{LoggingDefaults.NAME} is up. {len(self.bot.cogs)} of {LoggingDefaults.COG_COUNT} cogs running. Currently serving {len(self.bot.guilds)} servers.", "INFO")

def setup(bot):
    bot.add_cog(Events(bot))