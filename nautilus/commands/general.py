# ruff: noqa
def _welcome(bot, trigger):
    if trigger.sender != bot.settings.azura_cast.ctrl_channel:
        if trigger.nick != bot.nick:
            greeting = "Bienvenido a #radionautica"

