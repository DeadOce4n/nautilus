from requests.exceptions import HTTPError, ConnectionError
from sopel.tools import get_logger
from sopel.bot import Sopel
from sopel.trigger import Trigger
from ..utils.strings import streamers as streamers_strings, general as general_strings
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
        if not bot.memory["g"].get("streamers_service"):
            bot.memory["g"]["streamers_service"] = StreamersService(
                bot.config.AzuraCast.base_url,
                bot.config.AzuraCast.shortcode,
                bot.config.AzuraCast.api_key,
            )
        streamers_service: StreamersService = bot.memory["g"]["streamers_service"]

        def show(all: bool = False):
            streamers = ", ".join(
                [
                    s.display_name
                    for s in streamers_service.get_all()
                    if all or s.is_active
                ]
            )
            bot.say(streamers, trigger.sender)

        def create(*args):
            print("Create")

        def delete(*args):
            bot.say(", ".join(args), trigger.sender)

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
            "default": Command(
                [], lambda: bot.say("Comando desconocido :(", trigger.sender)
            ),
        }

        args: list[str] = [
            group
            for (i, group) in enumerate(trigger.groups())
            if group is not None and i != 1
        ]


        if len(args) < 2:
            for string in streamers_strings["ALL_ARGS_MISSING"]:
                bot.say(string, trigger.sender)

        commands.get(trigger.group(3), commands["default"]).exec(args)

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
        bot.say(f"Hacen falta argumentos: {data}", trigger.sender)
