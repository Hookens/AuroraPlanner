# Copyright (C) 2025 Hookens
# See the LICENSE file in the project root for details.

from discord.bot import Bot
from discord.ext import commands

from Debug.debughelpers import try_func_async
from Events.eventview import EventView

class Events(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    @try_func_async()
    async def on_ready (self):
        self.bot.add_view(EventView())

        cogcheck: int = 1
        
        if (logging := self.bot.get_cog("Logging")) is not None:
            cogcheck += 1
        if self.bot.get_cog("Embeds") is not None:
            cogcheck += 1
        if self.bot.get_cog("DebugMethods") is not None:
            cogcheck += 1
        if self.bot.get_cog("DebugCommands") is not None:
            cogcheck += 1
        if self.bot.get_cog("EventMethods") is not None:
            cogcheck += 1
        if self.bot.get_cog("EventCommands") is not None:
            cogcheck += 1
        
        if logging is not None:
            await logging.log_event(f"TFAScheduler is up. {cogcheck} of 7 cogs running. Currently serving {len(self.bot.guilds)} servers.", "INFO")

def setup(bot):
    bot.add_cog(Events(bot))