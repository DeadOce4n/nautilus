from sopel import config, bot, trigger
from sopel.tools import SopelMemory
from sopel.plugin import command
from .commands.streamers import djs as _djs


class AzuraCastSection(config.types.StaticSection):
    api_key = config.types.ValidatedAttribute("api_key")
    base_url = config.types.ValidatedAttribute("base_url")
    shortcode = config.types.ValidatedAttribute("shortcode")
    ctrl_channel = config.types.ValidatedAttribute("ctrl_channel")


def setup(bot: bot.Sopel):
    bot.config.define_section("AzuraCast", AzuraCastSection)
    bot.memory["g"] = SopelMemory()


def configure(config: config.Config):
    config.define_section("AzuraCast", AzuraCastSection, validate=False)


@command("djs")
def djs(bot: bot.Sopel, trigger: trigger.Trigger):
    return _djs(bot, trigger)
