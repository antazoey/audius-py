from functools import cached_property
from typing import Optional, Union

from audius.client_factory import ClientFactory, get_hosts
from audius.config import Config
from audius.player import Player
from audius.playlists import Playlists
from audius.tips import Tips
from audius.tracks import Tracks
from audius.users import Users


class Audius:
    def __init__(self, __config_or_name: Optional[Union[Config, str]] = None):
        self.config = (
            Config(app_name=__config_or_name)
            if isinstance(__config_or_name, str)
            else __config_or_name or Config.from_env()
        )
        self.factory = ClientFactory(self.config.app_name)
        self.player = Player(self)

    @property
    def app_name(self) -> str:
        return self.config.app_name

    @cached_property
    def client(self):
        """
        Get the configured client for this session.
        Will use the given host if present. Else will
        connect to a random host.
        """

        if self.config.host is not None:
            return self.factory.get_client(self.config.host)

        return self.factory.get_random_client()

    @cached_property
    def users(self) -> Users:
        return Users(self)

    @cached_property
    def playlists(self) -> Playlists:
        return Playlists(self)

    @cached_property
    def tracks(self) -> Tracks:
        return Tracks(self)

    @cached_property
    def tips(self) -> Tips:
        return Tips(self)

    @classmethod
    def get_hosts(cls):
        """
        Get all hosts available to connect to.
        """

        return get_hosts()
