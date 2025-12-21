# Copyright (C) 2025 Hookens
# See the LICENSE file in the project root for details.

from discord import ApplicationContext, Message, TextChannel
from discord.bot import Bot
from discord.ext import commands

from Utilities.datahelpers import Operation, LinkedOperation
from Utilities.constants import EmbedDefaults

from Debug.debughelpers import try_func_async

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Utilities.data import Data
    from Utilities.embeds import Embeds

class SharingMethods(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    def _get_cogs(self, include_embeds: bool = False, include_data: bool = False) -> tuple:
        embeds = self.bot.get_cog("Embeds") if include_embeds else None
        data = self.bot.get_cog("Data") if include_data else None
        
        if ((embeds is None and include_embeds) or 
            (data is None and include_data)):
            raise(ValueError("One or more cogs are missing.", embeds, data))
        
        return tuple(filter(None, (embeds, data)))

    async def parse_servers(self, servers: str) -> tuple[list[int], list[str]]:
        found: list[int] = []
        not_found: list[str] = []

        for part in servers.split(','):
            part = part.strip()

            if part.isdigit():
                guild_id = int(part)
                guild = await self.bot.fetch_guild(guild_id)

                if guild:
                    found.append(guild_id)
                else:
                    not_found.append(part)
            else:
                not_found.append(part)

        return (found, not_found)

    @try_func_async()
    async def share_event(self, ctx: ApplicationContext, eventid: int, servers: str, channel: TextChannel = None):
        data: 'Data'
        embeds: 'Embeds'
        (embeds, data) = self._get_cogs(True, True)

        #TODO: Check if already shared, if so append servers that aren't already allowed.

        message: Message = None
        try:
            if channel is not None:
                message = await channel.fetch_message(eventid)
            else:
                    message = await ctx.channel.fetch_message(eventid)
        except Exception:
            pass

        if message is None or not (message.author.id == self.bot.user.id and any(message.embeds[0].fields)):
            return embeds.generate_not_found_embed(channel)

        valid_guilds, _ = await self.parse_servers(servers)
        
        if len(valid_guilds) == 0:
            return embeds.generate_embed("No valid servers", "The server list you have provided contained no servers AuroraPlanner has access to.", EmbedDefaults.RED)
        
        await data.add_operation(message.id, channel.id, ctx.guild_id(), ','.join(valid_guilds))

        return embeds.generate_embed("Operation shared", f"The operation was shared.", EmbedDefaults.RED)

    @try_func_async()
    async def unshare_event(self, ctx: ApplicationContext, eventid: int, servers: str = None):
        data: 'Data'
        embeds: 'Embeds'
        (embeds, data) = self._get_cogs(True, True)

        linked_operations: list[LinkedOperation] = await data.get_linked_operations(eventid)

        for linked_operation in linked_operations:
            if servers is None or str(linked_operation.linked_guild_id) in servers:
                guild = await self.bot.fetch_guild(linked_operation.linked_guild_id)
                channel = await guild.fetch_channel(linked_operation.linked_channel_id)
                linked_event = await channel.fetch_message(linked_operation.linked_id)
                
                await linked_event.delete(reason="Operation has been unshared.")
                await data.delete_linked_operation(linked_operation.id, linked_operation.linked_guild_id)

        #TODO: Unshare from given server ids if populated, if left empty fully unshare.

def setup(bot: Bot):
    bot.add_cog(SharingMethods(bot))