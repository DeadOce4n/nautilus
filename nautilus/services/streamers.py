import json
import requests
from datetime import datetime
from dataclasses import dataclass
from ..utils.exceptions import UserNotFound
from ..classes.user import User


@dataclass
class UserCache:
    data: list[User]
    updated_at: datetime


class StreamersService:
    def __init__(self, base_url: str, shortcode: str, api_key: str, stale_time=180):
        self._base_url = base_url
        self._shortcode = shortcode
        self._api_key = api_key
        self._streamers: UserCache | None = None
        self._stale_time = stale_time
        self._base_headers = {"accept": "application/json", "X-API-Key": self._api_key}

    def _get_streamers(self):
        diff = (
            (datetime.now() - self._streamers.updated_at).total_seconds()
            if self._streamers
            else 0
        )
        if not self._streamers or diff >= self._stale_time:
            response = requests.get(
                f"{self._base_url}/station/{self._shortcode}/streamers",
                headers=self._base_headers,
                timeout=5,
            )
            response.raise_for_status()
            data = response.json()
            streamers = [User(**user) for user in data]
            self._streamers = UserCache(data=streamers, updated_at=datetime.now())
            return streamers
        else:
            return self._streamers.data

    def get_one(self, id: int | None = None, username: str | None = None):
        if username:
            streamers = self._get_streamers()
            for streamer in streamers:
                if streamer.streamer_username == username:
                    return streamer
            return None
        elif id:
            response = requests.get(
                f"{self._base_url}/station/{self._shortcode}/streamers/{id}",
                headers=self._base_headers,
            )
            response.raise_for_status()
            data = response.json()
            user = User(**data)
            return user

    def get_all(self):
        s = self._get_streamers()
        return s

    def create(self, username: str, password: str):
        headers = {**self._base_headers, "Content-Type": "application/json"}
        params = {
            "streamer_username": username,
            "streamer_password": password,
            "display_name": username,
            "is_active": True,
        }
        response = requests.post(
            f"{self._base_url}/station/{self._shortcode}/streamers",
            headers=headers,
            data=json.dumps(params),
        )
        response.raise_for_status()
        data = response.json()
        new_user = User(**data)
        if self._streamers:
            self._streamers.data.append(new_user)

    def _delete(self, id: int):
        response = requests.delete(
            f"{self._base_url}/station/{self._shortcode}/streamer/{id}",
            headers=self._base_headers,
        )
        response.raise_for_status()

    def _update(self, id: int, **params):
        headers = {**self._base_headers, "Content-Type": "application/json"}
        params = {**params}
        response = requests.put(
            f"{self._base_url}/station/{self._shortcode}/streamers/{id}",
            headers=headers,
            data=json.dumps(params),
        )
        response.raise_for_status()

    def delete(self, username: str):
        """
        Args:
            username (str): Username of the user to delete
        Raises:
            UserNotFound: If user does not exist
        """
        streamers = self._get_streamers()
        streamer = [s for s in streamers if s.streamer_username == username]
        if len(streamer) == 0:
            raise UserNotFound(f"Usuario {username} no existe")
        try:
            self._delete(streamer[0].id)
            self._streamers = None
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                raise UserNotFound(f"Usuario {username} no existe")

    def change_password(self, username: str, new_password: str):
        user = self.get_one(username=username)
        if not user:
            raise UserNotFound
        self._update(user.id, params={"password": new_password})
