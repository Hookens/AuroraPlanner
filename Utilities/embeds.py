# Copyright (C) 2025 Hookens
# See the LICENSE file in the project root for details.

from discord.bot import Bot
from discord.embeds import Embed
from discord.ext import commands

from Debug.debughelpers import try_func_async

class Embeds(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @try_func_async()
    async def generate_embed(self, title: str, description: str, color: int = 0xCC0000, image: str = None, footer: str = None, **kwargs) -> Embed:
        embed = Embed(title=title, description=description, colour=color)
        if image is not None:
            embed.set_thumbnail(url=image)
        if footer is not None:
            embed.set_footer(text=footer)
            
        for key, value in kwargs.items():
            embed.add_field(name=key, value=value, inline=False)

        return embed

    async def unexpected_error(self) -> Embed:
        return await self.generate_embed("Unexpected Error", f"TFAScheduler encountered an unexpected error.")

    async def cog_restarted(self, cog: str) -> Embed:
        return await self.generate_embed("Cog Restarted", f"`{cog}` cog was successfully restarted.", 0x00AA00)

    async def cog_restart_error(self, cog: str) -> Embed:
        return await self.generate_embed("Cog Restart Failed", f"`{cog}` cog could not be restarted.")

    async def generate_no_cog_found(self, cog: str) -> Embed:
        return await self.generate_embed("Cog Not Found", f"`{cog}` cog was not found. Double-check availability.", 0xCCAA00)

def setup(bot):
    bot.add_cog(Embeds(bot))