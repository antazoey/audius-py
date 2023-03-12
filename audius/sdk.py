import os
from functools import cached_property
from typing import Optional

from audius.client_factory import ClientFactory
from audius.exceptions import UnknownAppError
from audius.playlists import Playlists
from audius.users import Users

AUDIUS_APP_NAME_ENV_VAR = "AUDIUS_APP_NAME"


class Audius:
    def __init__(self, app_name: str, host: Optional[str] = None):
        self.app_name = app_name
        self.factory = ClientFactory(app_name)
        self.host = host

    @classmethod
    def from_env(cls):
        value = os.environ.get(AUDIUS_APP_NAME_ENV_VAR)
        if not value:
            raise UnknownAppError()

        return cls(value, host=os.environ.get("AUDIUS_HOST_NAME"))

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

    def get_hosts(self):
        """
        Get all hosts available to connect to.
        """

        return self.factory.get_hosts()
