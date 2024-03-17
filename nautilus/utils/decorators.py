import functools
from typing import Callable, Literal
from sopel import bot, trigger
from sopel.tools import Identifier, get_logger

from nautilus.utils.strings import (
    GENERAL_REQUIRE_SPECIFIC_CHANNEL,
    GENERAL_REQUIRE_PRIVMSG,
)


LOGGER = get_logger("nautilus")


def allow_from(
    type: Literal["public_channel"] | Literal["control_channel"] | Literal["privmsg"],
):
    def decorator_allow_from(func: Callable[[bot.Sopel, trigger.Trigger], None]):
        @functools.wraps(func)
        def wrapper_allow_from(
            bot_instance: bot.Sopel, trigger_instance: trigger.Trigger
        ):
            if type == "privmsg" and not trigger_instance.is_privmsg:
                bot_instance.say(
                    GENERAL_REQUIRE_PRIVMSG.format(trigger_instance.group(0)),
                    trigger_instance.sender,
                )
            elif type == "control_channel" and (
                trigger_instance.sender
                != Identifier(bot_instance.config.AzuraCast.control_channel)
                or trigger_instance.is_privmsg
            ):
                bot_instance.say(
                    GENERAL_REQUIRE_SPECIFIC_CHANNEL.format(
                        trigger_instance.group(0),
                        bot_instance.config.AzuraCast.control_channel,
                    ),
                    trigger_instance.sender,
                )
            elif type == "public_channel" and (
                trigger_instance.sender
                == Identifier(bot_instance.config.AzuraCast.control_channel)
                or trigger_instance.is_privmsg
            ):
                bot_instance.say(
                    GENERAL_REQUIRE_SPECIFIC_CHANNEL.format(
                        trigger_instance.group(0),
                        bot_instance.config.AzuraCast.public_channel,
                    ),
                    trigger_instance.sender,
                )
            else:
                return func(bot_instance, trigger_instance)

        return wrapper_allow_from

    return decorator_allow_from
