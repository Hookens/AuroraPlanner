class Env:
    API_TOKEN = "" #PUT YOUR API TOKEN HERE
    DBHST = "" #PUT YOUR DATABASE HOST HERE
    DBUSR = "" #PUT YOUR DATABASE USER HERE
    DBPWD = "" #PUT YOUR DATABASE PWD HERE

class LoadOrder:
    COGS = [
        "Debug.logging",
        "Utilities.events",
        "Utilities.embeds",
        "Debug.debugmethods",
        "Debug.debugcommands",
        "Help.helpmethods",
        "Help.helpcommands",
        "Events.eventmethods",
        "Events.eventcommands",
    ]

class LoggingDefaults:
    NAME = "Aurora Planner"
    CHANNEL = 0 #PUT YOUR LOG CHANNEL ID HERE
    PING = 0 #PUT YOUR USER ID HERE
    COG_COUNT = len(LoadOrder.COGS)

class EmbedDefaults:
    WHITE = 0xFFFFFF
    GREEN = 0x00CC00
    RED = 0xCC0000
    ORANGE = 0xFFAA00
    PURPLE = 0x8663FC

class HelpDefaults:
    HELP_OPTIONS = [
        "About Aurora",
        "Scheduling Events",
        "Editing Events",
    ]

    COLOR = EmbedDefaults.PURPLE
    AUTHOR = LoggingDefaults.PING
    SUPPORT_ME = "[It's entirely optional](https://ko-fi.com/hookens)"

class DebugLists:
    GUILDS = [
        0, #PUT YOUR DEBUG GUILD ID HERE
    ]

    COGS = [
        "DebugCommands",
        "DebugMethods",
        "Logging",
        "HelpCommands",
        "HelpMethods",
        "EventCommands",
        "EventMethods",
        "Embeds",
        "Events",
    ]

class DebugTexts:
    C_ANNOUNCE = "Make an announcement embed."
    C_SHUTDOWN = "Ends the bot thread."
    C_RELOAD = "Reload a cog."
    C_STATUS = "Get bot cogs' status."

    F_TITLE = "Title for the announcement."
    F_DESCRIPTION = "Description for the announcement."
    F_COG = "Cog that needs to be reloaded."

class HelpTexts:
    C_HELP = "Show the help menu."
    F_PUBLIC = "If you wish to make this message public."

    O_ABOUT = "Links to resources and other info."
    O_SCHEDULING = "Commands for event creation and scheduling."
    O_EDITING = "Commands for event edition."

class EventTexts:
    S_SCHEDULE = "Event related commands"

    C_ADD = "Schedule a new event."
    F_TITLE = "The title of the event."
    F_DESC = "The description of the event."
    F_TIME = "The date and time of the event, in 'DD-MM-YYYY HH:mm' format, on UTC."
    F_MODTITLE = "The title of the modpack."
    F_MODLINK = "The link to the modpack."
    F_ATTENDANCE = "The minimum attendance for the event."
    F_DLC = "The required DLC for the event."
    F_DETAILS = "The additional details (gear/year/team composition/etc) for the event."
    F_IMAGE = "The image preview of the event."
    F_PING = "Role to ping with the event."
    F_CHANNEL = "A different channel in which to post the event."

    C_EDIT = "Edit a previously scheduled event."
    F_MESSAGE = "The id of the event (message)."
    F_DIFFCHANNEL = "The different channel in which the event is."

    C_COPY = "Copy a previously scheduled event into its original command form."