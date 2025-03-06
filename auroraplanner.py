# Copyright (C) 2025 Hookens
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKENTFASCHEDULER = os.getenv('DISCORD_TOKEN_TFASCHEDULER')

intents = discord.Intents().default()
tfaschedulerClient = commands.Bot(intents=intents, help_command=None)

tfaschedulerClient.load_extension("Debug.logging")
tfaschedulerClient.load_extension("Utilities.events")
tfaschedulerClient.load_extension("Utilities.embeds")
tfaschedulerClient.load_extension("Debug.debugcommands")
tfaschedulerClient.load_extension("Debug.debugmethods")
tfaschedulerClient.load_extension("Events.eventcommands")
tfaschedulerClient.load_extension("Events.eventmethods")

tfaschedulerClient.run(TOKENTFASCHEDULER)