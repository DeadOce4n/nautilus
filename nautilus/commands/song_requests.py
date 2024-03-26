import shlex
import threading
import os
from datetime import datetime, timedelta
from typing import cast
from sopel.bot import Sopel, Trigger
from sopel.tools import Identifier, get_logger
from sopel.formatting import bold

from ..utils.strings import (
    GENERAL_MISSING_ARGS,
    SONG_REQUESTS_EXAMPLE,
    SONG_REQUESTS_NEW_REQUEST,
    SONG_REQUESTS_UNRECOGNIZED_ARGS,
    SONG_REQUESTS_USER_HAS_REQUEST,
)
from ..utils.classes import ArgumentParser, UnrecognizedArgs

LOGGER = get_logger("nautilus")


REQUEST_INTERVAL = 10.0 if os.getenv("ENV", "production") == "development" else 300.0


def request_song_handler(bot: Sopel, trigger: Trigger):
    try:
        parser = ArgumentParser(add_help=False, exit_on_error=False)
        parser.add_argument("-a", "--artist", "--artista", type=str)
        parser.add_argument("-s", "--song", "-c", "--cancion", "--canción", type=str)

        raw_command_args = shlex.split(trigger.groups()[1])

        args = parser.parse_args(args=raw_command_args)

        missing_args: list[str] = []

        if args.artist is None:
            missing_args.append("artista")
        if args.song is None:
            missing_args.append("canción")

        if len(missing_args) > 0:
            bot.say(
                GENERAL_MISSING_ARGS.format(
                    ", ".join([bold(f'"{arg}"') for arg in missing_args])
                ),
                trigger.sender,
            )
            for string in SONG_REQUESTS_EXAMPLE:
                bot.say(string, trigger.sender)
            return

        if "users_with_request" not in bot.memory["g"]:
            bot.memory["g"]["users_with_request"] = {}

        users_with_request: dict[Identifier, datetime] = bot.memory["g"][
            "users_with_request"
        ]

        cast(dict, users_with_request)

        if trigger.nick not in users_with_request:
            bot.memory["g"]["users_with_request"][trigger.nick] = datetime.now()

            bot.say(
                SONG_REQUESTS_NEW_REQUEST.format(
                    # TODO: use active DJ nick in here
                    "DJ",
                    trigger.nick,
                    args.song,
                    args.artist,
                ),
                Identifier(bot.config.AzuraCast.control_channel),
            )

            threading.Timer(
                interval=REQUEST_INTERVAL,
                function=lambda: bot.memory["g"]["users_with_request"].pop(
                    trigger.nick
                ),
            ).start()
        else:
            requested_at = cast(
                datetime, bot.memory["g"]["users_with_request"][trigger.nick]
            )
            remaining_time = (
                requested_at + timedelta(seconds=REQUEST_INTERVAL)
            ) - datetime.now()

            is_in_minutes = remaining_time.seconds > 60

            bot.say(
                SONG_REQUESTS_USER_HAS_REQUEST.format(
                    trigger.nick,
                    f"{int(remaining_time.seconds / 60)} minutos"
                    f" {remaining_time.seconds % 60} segundos"
                    if is_in_minutes
                    else f"{remaining_time.seconds} segundos",
                ),
                trigger.sender,
            )

    except UnrecognizedArgs as err:
        LOGGER.error(err)
        bot.say(
            SONG_REQUESTS_UNRECOGNIZED_ARGS.format(
                ", ".join([bold(f'"{arg}"') for arg in err.unrecognized_args])
            ),
            trigger.sender,
        )
