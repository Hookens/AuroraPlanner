# Copyright (C) 2025 Hookens
# See the LICENSE file in the project root for details.

from discord.bot import Bot
from discord.embeds import Embed
from discord.ext import commands

from Debug.debughelpers import try_func_async
from Utilities.constants import HelpDefaults, HelpTexts, EventTexts


class HelpMethods(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @try_func_async(embed=True)
    async def generate_help(self, menu: str = "") -> Embed:
        if menu == HelpDefaults.HELP_OPTIONS[1]:
            embed = self.generate_help_event_creation()
        elif menu == HelpDefaults.HELP_OPTIONS[2]:
            embed = self.generate_help_event_edition()
        else:
            embed = self.generate_help_about()

        embed.color = HelpDefaults.COLOR
        author = self.bot.get_user(HelpDefaults.AUTHOR)
        embed.set_footer(text=f"Developed by {author.name}", icon_url=author.avatar.url)
        return embed

    def generate_help_about(self):
        embed = Embed(title="About Aurora Planner", description="Aurora Planner is a simple ArmA-focused event planning bot.")

        embed.add_field(name="Support my work", value=HelpDefaults.SUPPORT_ME, inline=True)

        embed.add_field(name="Scheduling Events", value=HelpTexts.O_SCHEDULING, inline=False)
        embed.add_field(name="Editing Events", value=HelpTexts.O_EDITING, inline=False)

        return embed
    
    def generate_help_event_creation(self):
        embed = Embed(title="Event  •  Scheduling", description=HelpTexts.O_SCHEDULING)

        command: str = (
            "</schedule add:1201186072080695388>"
        )
        parameters: str = (
            "Parameters marked with an asterisk are required.\n"
            f"- `title`* - {EventTexts.F_TITLE}\n"
            f"- `description`* - {EventTexts.F_DESC}\n"
            f"- `time`* - {EventTexts.F_TIME}\n"
            f"- `modpacktitle` - {EventTexts.F_MODTITLE}\n"
            f"- `modpacklink` - {EventTexts.F_MODLINK}\n"
            f"- `minimumattendance` - {EventTexts.F_ATTENDANCE}\n"
            f"- `requireddlc` - {EventTexts.F_DLC}\n"
            f"- `additionaldetails` - {EventTexts.F_DETAILS}\n"
            f"- `imagelink` - {EventTexts.F_IMAGE}\n"
            f"- `ping` - {EventTexts.F_PING}\n"
            f"- `channel` - {EventTexts.F_CHANNEL}\n"
        )
        tips : str = (
            "- You can copy an existing schedule using </schedule copy:1201186072080695388>.\n"
            "- Fields support standard discord markdown.\n"
            "- Newlines can be added to the description and the additional details section using `\\n`.\n"
        )

        embed.add_field(name="Command", value=command, inline=False)
        embed.add_field(name="Parameters", value=parameters, inline=False)
        embed.add_field(name="Tips", value=tips, inline=False)

        return embed
    
    def generate_help_event_edition(self):
        embed = Embed(title="Event  •  Editing", description=HelpTexts.O_EDITING)

        command: str = (
            "</schedule edit:1201186072080695388>"
        )
        parameters: str = (
            "Parameters marked with an asterisk are required.\n"
            f"- `messageid`* - {EventTexts.F_MESSAGE}\n"
            f"- `title` - {EventTexts.F_TITLE}\n"
            f"- `description` - {EventTexts.F_DESC}\n"
            f"- `time` - {EventTexts.F_TIME}\n"
            f"- `modpacktitle` - {EventTexts.F_MODTITLE}\n"
            f"- `modpacklink` - {EventTexts.F_MODLINK}\n"
            f"- `minimumattendance` - {EventTexts.F_ATTENDANCE}\n"
            f"- `requireddlc` - {EventTexts.F_DLC}\n"
            f"- `additionaldetails` - {EventTexts.F_DETAILS}\n"
            f"- `imagelink` - {EventTexts.F_IMAGE}\n"
            f"- `channel` - {EventTexts.F_DIFFCHANNEL}\n"
        )
        tips : str = (
            "- Ignored parameters will not empty current fields.\n"
            "- Fields can be emptied by adding them to the command but leaving them empty.\n"
            "- Fields support standard discord markdown.\n"
            "- Newlines can be added to the description and the additional details section using `\\n`.\n"
        )

        embed.add_field(name="Command", value=command, inline=False)
        embed.add_field(name="Parameters", value=parameters, inline=False)
        embed.add_field(name="Tips", value=tips, inline=False)

        return embed

def setup(bot):
    bot.add_cog(HelpMethods(bot))