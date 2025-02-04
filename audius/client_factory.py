from random import randint

import requests

from audius.client import Client


def get_hosts() -> list[str]:
    response = requests.get("https://api.audius.co")
    response.raise_for_status()
    return response.json().get("data", [])


class ClientFactory:
    def __init__(self, app_name: str):
        self.app_name = app_name

    def get_random_client(self) -> Client:
        hosts = get_hosts()
        index = randint(0, len(hosts) - 1)
        choice = hosts[index]
        return self.get_client(choice)

    def get_client(self, host: str) -> Client:
        return Client(self.app_name, host)
