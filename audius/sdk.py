import os
from functools import cached_property
from typing import Optional

from audius.client_factory import ClientFactory
from audius.player import Player
from audius.playlists import Playlists
from audius.tips import Tips
from audius.tracks import Tracks
from audius.users import Users

AUDIUS_APP_NAME_ENV_VAR = "AUDIUS_APP_NAME"
AUDIUS_HOST_NAME_ENV_VAR = "AUDIUS_HOST_NAME"
DEFAULT_APP_NAME = "audius-py"


class Audius:
    def __init__(self, app: Optional[str] = None, host: Optional[str] = None):
        self.app_name: str = (
            app if app is not None else os.environ.get(AUDIUS_APP_NAME_ENV_VAR, DEFAULT_APP_NAME)
        )
        self.factory = ClientFactory(self.app_name)
        self.host = host or os.environ.get(AUDIUS_HOST_NAME_ENV_VAR)
        self.player = Player()

    @cached_property
    def client(self):
        """
        Get the configured client for this session.
        Will use the given host if present. Else will
        connect to a random host.
        """

        if self.host is not None:
            return self.factory.get_client(self.host)

        return self.factory.get_random_client()

    @cached_property
    def users(self) -> Users:
        return Users(self.client)

    @cached_property
    def playlists(self) -> Playlists:
        return Playlists(self.client)

    @cached_property
    def tracks(self) -> Tracks:
        return Tracks(self.client, self.player)

    @cached_property
    def tips(self) -> Tips:
        return Tips(self.client)

    def get_hosts(self):
        """
        Get all hosts available to connect to.
        """

        return self.factory.get_hosts()
