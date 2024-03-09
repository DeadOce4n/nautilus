from requests.exceptions import HTTPError, ConnectionError
from sopel.tools import get_logger
from sopel.bot import Sopel
from sopel.trigger import Trigger
from uuid import uuid4

from ..utils.strings import (
    GENERAL_MISSING_ARGS,
    STREAMERS_AVAILABLE_ACTIONS,
    STREAMERS_CONFIRM_DELETE,
    STREAMERS_DELETE_SUCCESS,
    STREAMERS_ERROR_MISSING_TOKEN,
    STREAMERS_ERROR_WRONG_TOKEN,
    STREAMERS_UNKNOWN_COMMAND,
    STREAMERS_UNKNOWN_ERROR,
    streamers as streamers_strings,
    general as general_strings,
)
from ..utils.exceptions import UserNotFound, MissingRequiredArgs
from ..services.streamers import StreamersService
from ..classes.command import Command
from ..classes.param import Param

LOGGER = get_logger("nautilus")


def djs(bot: Sopel, trigger: Trigger):
    """
    Commands:
    !djs listar [todos]
    !djs registrar usuario contraseña
    !djs borrar usuario [token]
    !djs cambiar-contraseña usuario contraseña
    """
    try:
        if "streamers_service" not in bot.memory["g"]:
            bot.memory["g"]["streamers_service"] = StreamersService(
                bot.config.AzuraCast.base_url,
                bot.config.AzuraCast.shortcode,
                bot.config.AzuraCast.api_key,
            )
        if not bot.memory["g"].get("pending_deletion"):
            bot.memory["g"]["pending_deletion"] = {}

        streamers_service: StreamersService = bot.memory["g"]["streamers_service"]

        assert isinstance(streamers_service, StreamersService)

        def show(all: bool = False):
            streamers = ", ".join(
                [
                    s.display_name
                    for s in streamers_service.get_all()
                    if all or s.is_active
                ]
            )
            bot.say(streamers, trigger.sender)

        def create(username: str, password: str):
            try:
                streamers_service.create(username, password)
                LOGGER.info(f"Registered new DJ: {username}")
                bot.say(
                    streamers_strings["DJ_REGISTRATION_SUCCESS"].format(username),
                    trigger.sender,
                )
            except HTTPError as e:
                LOGGER.error(e)
                bot.say(
                    streamers_strings["DJ_REGISTRATION_FAILED"],
                    trigger.sender,
                )

        def delete(username: str, code: str | None = None):
            if username not in bot.memory["g"]["pending_deletion"]:
                token = str(uuid4().time_low)
                bot.memory["g"]["pending_deletion"][username] = token
                bot.say(
                    STREAMERS_CONFIRM_DELETE.format(username, username, token),
                    trigger.sender,
                )
            elif code is None:
                bot.say(STREAMERS_ERROR_MISSING_TOKEN, trigger.sender)
            elif code != bot.memory["g"]["pending_deletion"][username]:
                bot.say(STREAMERS_ERROR_WRONG_TOKEN, trigger.sender)
            else:
                try:
                    streamers_service.delete(username)
                    bot.memory["g"]["pending_deletion"].pop(username)
                    bot.say(STREAMERS_DELETE_SUCCESS.format(username), trigger.sender)
                except UserNotFound as e:
                    LOGGER.error(e)
                    bot.say(
                        streamers_strings["USER_NOT_EXISTS"].format(username),
                        trigger.sender,
                    )

        def change_password():
            print("Change password")

        commands: dict[str, Command] = {
            "listar": Command([Param("todos")], show),
            "registrar": Command(
                [Param("usuario", True), Param("contraseña", True)], create
            ),
            "borrar": Command([Param("usuario", True), Param("token")], delete),
            "cambiar-contraseña": Command(
                [Param("usuario", True), Param("contraseña", True)],
                change_password,
            ),
        }

        args: list[str] = [
            group
            for (i, group) in enumerate(trigger.groups())
            if group is not None and i != 1
        ]

        if len(args) < 2:
            for string in STREAMERS_AVAILABLE_ACTIONS:
                bot.say(string, trigger.sender)

        command_name = trigger.group(3)

        if command_name is not None and command_name not in commands:
            bot.say(STREAMERS_UNKNOWN_COMMAND.format(command_name), trigger.sender)
        elif command_name is not None:
            commands[command_name].exec(args)

    except ConnectionError as err:
        LOGGER.error(err)
        bot.say(general_strings["CONN_ERROR"], trigger.sender)
    except HTTPError as err:
        LOGGER.error(err)
        bot.say(err.strerror, trigger.sender)
    except UserNotFound as err:
        LOGGER.error(err)
        bot.say("Hola", trigger.sender)
    except MissingRequiredArgs as err:
        data = None
        if isinstance(err.missing_args, list):
            data = ", ".join([arg.name for arg in err.missing_args])
        else:
            data = err.missing_args.name
        bot.say(GENERAL_MISSING_ARGS.format(data), trigger.sender)
    except AssertionError as err:
        LOGGER.error(err)
        bot.say(STREAMERS_UNKNOWN_ERROR, trigger.sender)
