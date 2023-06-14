import pytest
import responses

from ..utils.exceptions import MissingRequiredArgs
from ..classes.command import Command
from ..classes.param import Param
from ..services.streamers import StreamersService
from ..tests.utils.func import get_random_string


def test_missing_required_args():
    def login(user: str, password: str):
        print(f"Hello, {user}, your password is: {password}")

    command = Command([Param("usuario", True), Param("contraseña", True)], login)

    with pytest.raises(MissingRequiredArgs):
        command.exec(["!djs", "cambiar-contraseña", "asdfghjkl"])


@responses.activate
def test_streamers_service_get_all():
    options = {
        "base_url": "https://radionautica.xyz",
        "shortcode": "radionautica",
        "api_key": get_random_string(36),
    }

    streamers_service = StreamersService(**options, stale_time=180)

    responses.add(
        responses.GET,
        f"{options['base_url']}/station/{options['shortcode']}/streamers",
        json=[
            {
                "id": 1,
                "streamer_username": "DeadOcean",
                "streamer_password": "",
                "display_name": "DeadOcean",
                "comments": "",
                "is_active": True,
                "enforce_schedule": False,
                "reactivate_at": 131231,
                "schedule_items": [],
                "art": get_random_string(25),
                "art_updated_at": 0,
                "has_custom_art": False,
                "links": [],
            },
            {
                "id": 2,
                "streamer_username": "Gusy",
                "streamer_password": "",
                "display_name": "Gusy",
                "comments": "",
                "is_active": True,
                "enforce_schedule": False,
                "reactivate_at": 131231,
                "schedule_items": [],
                "art": get_random_string(25),
                "art_updated_at": 0,
                "has_custom_art": False,
                "links": [],
            },
        ],
        status=200,
    )

    users = streamers_service.get_all()

    assert len(users) > 0

@responses.activate
def test_streamers_service_get_one():
    assert True
