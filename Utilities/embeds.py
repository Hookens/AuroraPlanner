# Copyright (C) 2025 Hookens
# See the LICENSE file in the project root for details.

from discord import TextChannel
from discord.bot import Bot
from discord.embeds import Embed
from discord.ext import commands

from Utilities.constants import EmbedDefaults

class Embeds(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    def generate_embed(self, title: str, description: str, color: int = EmbedDefaults.RED, image: str = None, footer: str = None, **kwargs) -> Embed:
        embed = Embed(title=title, description=description, colour=color)
        if image is not None:
            embed.set_thumbnail(url=image)
        if footer is not None:
            embed.set_footer(text=footer)
            
        for key, value in kwargs.items():
            embed.add_field(name=key, value=value, inline=False)

        return embed
    
    def generate_not_found_embed(self, channel: TextChannel | None):
        return self.generate_embed("Event edition error", f"No event with the provided ID was found { f'in {channel.mention}' if channel is not None else 'in the current channel'}.", EmbedDefaults.RED)

    def unexpected_error(self) -> Embed:
        return self.generate_embed("Unexpected Error", f"TFAScheduler encountered an unexpected error.")

    def cog_restarted(self, cog: str) -> Embed:
        return self.generate_embed("Cog Restarted", f"`{cog}` cog was successfully restarted.", EmbedDefaults.GREEN)

    def cog_restart_error(self, cog: str) -> Embed:
        return self.generate_embed("Cog Restart Failed", f"`{cog}` cog could not be restarted.")

    def generate_no_cog_found(self, cog: str) -> Embed:
        return self.generate_embed("Cog Not Found", f"`{cog}` cog was not found. Double-check availability.", EmbedDefaults.ORANGE)

def setup(bot):
    bot.add_cog(Embeds(bot))