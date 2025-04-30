# Copyright (C) 2025 Hookens
# See the LICENSE file in the project root for details.

class Operation:
    def __init__(self, id: str, channel_id: str, guild_id: str, allowed_guild_ids: str):
        self.id: int = int(id)
        self.channel_id = int(channel_id)
        self.guild_id = int(guild_id)
        self.allowed_guild_ids = [int(id) for id in allowed_guild_ids.split(",")]

class LinkedOperation:
    def __init__(self, id: str, linked_id: str, linked_channel_id: str, linked_guild_id: str):
        self.id: int = int(id)
        self.linked_id: int = int(linked_id)
        self.linked_channel_id = int(linked_channel_id)
        self.linked_guild_id = int(linked_guild_id)