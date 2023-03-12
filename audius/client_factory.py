from functools import cached_property
from random import randint
from typing import List, Optional

from requests import Session

from audius.client import Client
from audius.session import create_session


class ClientFactory:
    _session: Optional[Session] = None

    @cached_property
    def session(self):
        if self._session is None:
            self._session = create_session()

        return self._session

    def get_hosts(self) -> List[str]:
        response = self.session.get("https://api.audius.co")
        host_list = response.json().get("data", [])
        return host_list

    def get_random_client(self) -> Client:
        hosts = self.get_hosts()
        index = randint(0, len(hosts) - 1)
        choice = hosts[index]
        return self.get_client(choice)

    def get_client(self, host: str) -> Client:
        return Client(host)
