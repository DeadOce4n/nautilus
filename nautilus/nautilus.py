from sopel import config, bot, trigger
from sopel.tools import SopelMemory
from sopel.plugin import command

from nautilus.commands.song_requests import request_song_handler

from .utils.decorators import allow_from
from .commands.streamers import djs_handler


class AzuraCastSection(config.types.StaticSection):
    api_key = config.types.ValidatedAttribute("api_key")
    base_url = config.types.ValidatedAttribute("base_url")
    shortcode = config.types.ValidatedAttribute("shortcode")
    control_channel = config.types.ValidatedAttribute("control_channel")
    public_channel = config.types.ValidatedAttribute("public_channel")


def setup(bot: bot.Sopel):
    bot.config.define_section("AzuraCast", AzuraCastSection)
    bot.memory["g"] = SopelMemory()


def configure(config: config.Config):
    config.define_section("AzuraCast", AzuraCastSection, validate=False)


@command("djs")
@allow_from("privmsg")
def djs(bot: bot.Sopel, trigger: trigger.Trigger):
    return djs_handler(bot, trigger)


@command("pedir")
@allow_from("public_channel")
def request_song(bot: bot.Sopel, trigger: trigger.Trigger):
    return request_song_handler(bot, trigger)
