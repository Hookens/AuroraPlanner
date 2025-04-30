# Copyright (C) 2025 Hookens
# See the LICENSE file in the project root for details.

from discord.bot import Bot
from discord.ext import commands
from mysql import connector
import os

from Utilities.constants import Env
from Utilities.datahelpers import Operation, LinkedOperation

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Debug.logging import Logging

HOST = os.getenv(Env.DBHST)
USER = os.getenv(Env.DBUSR)
PASSWORD = os.getenv(Env.DBPWD)
DATABASE = USER

DB_CONFIG = {
    'host': HOST,
    'user': USER,
    'password': PASSWORD,
    'database': DATABASE,
}


class Data(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        
    def _get_db_connection(self):
        return connector.connect(**DB_CONFIG)
    
    async def _log_sql_event(self, event: str, type: str):
        logging: 'Logging'
        if (logging := self.bot.get_cog("Logging")) is not None:
            await logging.log_event(event, type)
    
    async def _log_sql_error(self, e: Exception, method: str, *args):
        logging: 'Logging'
        if (logging := self.bot.get_cog("Logging")) is not None:
            await logging.log_error("'SQLError'", f"Data - {method}", e, *args)

    async def _execute_write_operation(self, proc_name: str, *args) -> bool:
        try:
            with self._get_db_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.callproc(proc_name, args)
                    connection.commit()
                    return True
                
        except Exception as e:
            await self._log_sql_error(e, proc_name, *args)
            return False

    async def _execute_read_operation(self, proc_name: str, *args):
        try:
            with self._get_db_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.callproc(proc_name, args)
                    for result in cursor.stored_results():
                        allowed_roles=result.fetchall()
                    return allowed_roles
                
        except Exception as e:
            await self._log_sql_error(e, proc_name, *args)
            return None

    async def add_operation(self, id: str, channel_id: str, guild_id: str, allowed_guild_ids: str) -> bool:
        await self._log_sql_event(f"Shared O'{channel_id}/{id}' with A'{allowed_guild_ids}' in G'{guild_id}", "INFO")
        return await self._execute_write_operation("AuroraAddOperation", id, channel_id, guild_id, allowed_guild_ids)

    async def delete_operation(self, id: int) -> bool:
        await self._log_sql_event(f"Removed O'{id}'", "INFO")
        return await self._execute_write_operation("AuroraDeleteOperation", id)

    async def add_linked_operation(self, id: str, linked_id: str, linked_channel_id: str, linked_guild_id: str) -> bool:
        await self._log_sql_event(f"Linked A'{linked_channel_id}/{linked_id}' to O'{id}' in G'{linked_guild_id}", "INFO")
        return await self._execute_write_operation("AuroraAddLinkedOperation", id, linked_id, linked_channel_id, linked_guild_id)

    async def delete_linked_operation(self, id: str, linked_guild_id: str) -> bool:
        await self._log_sql_event(f"Removed link to O'{id}' in G'{linked_guild_id}", "INFO")
        return await self._execute_write_operation("AuroraDeleteLinkedOperation", id)

    async def get_linked_operations(self, id: str) -> list[LinkedOperation]:
        result = await self._execute_read_operation("AuroraGetLinkedOperations", id)
        return [LinkedOperation(
            id=row[0],
            linked_id=row[1],
            linked_channel_id=row[2],
            linked_guild_id=row[3]
            ) for row in result] if result is not None else None

    async def is_linking_allowed(self, id: str) -> bool:
        return bool((await self._execute_read_operation("AuroraIsLinkingAllowed", id))[0][0])

def setup(bot):
    bot.add_cog(Data(bot))