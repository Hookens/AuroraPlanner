# Copyright (C) 2025 Hookens
# See the LICENSE file in the project root for details.

from discord import ButtonStyle
from discord.embeds import Embed
from discord.interactions import Interaction
from discord.ui import View, button, Button
from discord.user import User
import re

class EventView(View):
    def __init__(self):
        super().__init__(timeout=None)

    def remove_user(self, user: User, embed: Embed) -> Embed:
       value5 = re.sub('\n\n+', '\n', embed.fields[5].value.replace(f"{user.mention}", "")) or "-"
       value6 = re.sub('\n\n+', '\n', embed.fields[6].value.replace(f"{user.mention}", "")) or "-"
       value7 = re.sub('\n\n+', '\n', embed.fields[7].value.replace(f"{user.mention}", "")) or "-"

       count5 = 0 if value5 == "-" else len(value5.splitlines())
       count6 = 0 if value6 == "-" else len(value6.splitlines())
       count7 = 0 if value7 == "-" else len(value7.splitlines())

       namevalue5 = '' if count5 == 0 else f" ({count5})"
       namevalue6 = '' if count6 == 0 else f" ({count6})"
       namevalue7 = '' if count7 == 0 else f" ({count7})"

       name5 = f":white_check_mark: Accepted{namevalue5}"
       name6 = f":no_entry_sign: Declined{namevalue6}"
       name7 = f":grey_question: Tentative{namevalue7}"

       embed.set_field_at(index=5, name=name5, value=value5)
       embed.set_field_at(index=6, name=name6, value=value6)
       embed.set_field_at(index=7, name=name7, value=value7)
       
       return embed

    def add_user(self, field: int, user: User, embed: Embed) -> Embed:
        embed = self.remove_user(user, embed)

        name: str = ""
        if field == 5:
           name = ":white_check_mark: Accepted"
        elif field == 6:
           name = ":no_entry_sign: Declined"
        else:
           name = ":grey_question: Tentative"

        current = embed.fields[field].value
        empty = current == "-"

        fieldvalue: str = re.sub('\n\n+', '\n', (current if not empty else "")+ (f"\n{user.mention}"))

        namevalue = 1 if empty else len(fieldvalue.splitlines())

        name = f"{name} ({namevalue})"
           
        embed.set_field_at(index=field, name=name, value=fieldvalue)

        return embed

    @button(label="Accept", style=ButtonStyle.secondary, emoji="<:accepted:895317878092472402>", custom_id="tfasbtn_accept")
    async def accept_callback(self, button: Button, interaction: Interaction):
      await interaction.message.edit(embed=self.add_user(5, interaction.user, interaction.message.embeds[0]))
      await interaction.response.send_message(content="Vote noted ✅", delete_after=3, ephemeral=True)


    @button(label="Decline", style=ButtonStyle.secondary, emoji="<:declined:895317878398660639>", custom_id="tfasbtn_decline")
    async def decline_callback(self, button: Button, interaction: Interaction):
      await interaction.message.edit(embed=self.add_user(6, interaction.user, interaction.message.embeds[0]))
      await interaction.response.send_message(content="Vote noted ✅", delete_after=3, ephemeral=True)

    @button(label="Tentative", style=ButtonStyle.secondary, emoji="<:tentative:895317878214131753>", custom_id="tfasbtn_tentative")
    async def tentative_callback(self, button: Button, interaction: Interaction):
      await interaction.message.edit(embed=self.add_user(7, interaction.user, interaction.message.embeds[0]))
      await interaction.response.send_message(content="Vote noted ✅", delete_after=3, ephemeral=True)