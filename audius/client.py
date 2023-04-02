from functools import cached_property
from typing import TYPE_CHECKING

from requests import Response, Session

if TYPE_CHECKING:
    from audius.config import Config
    from audius.playlists import Playlists
    from audius.sdk import Audius
    from audius.tips import Tips
    from audius.tracks import Tracks
    from audius.users import Users


class API:
    def __init__(self, sdk: "Audius"):
        self.sdk = sdk

    @property
    def client(self) -> "Client":
        return self.sdk.client

    @property
    def config(self) -> "Config":
        return self.sdk.config

    @property
    def playlists(self) -> "Playlists":
        return self.sdk.playlists

    @property
    def tips(self) -> "Tips":
        return self.sdk.tips

    @property
    def tracks(self) -> "Tracks":
        return self.sdk.tracks

    @property
    def users(self) -> "Users":
        return self.sdk.users

    def _handle_id(self, _id: str) -> str:
        return self.config.aliases[_id] if _id in self.config.aliases else _id


class Client:
    def __init__(self, app_name: str, host_address: str):
        self.app_name = app_name
        self.host_address = host_address

    @cached_property
    def session(self) -> Session:
        return Session()

    def get(self, url: str, **kwargs) -> dict:
        kwargs["params"] = kwargs.get("params", {})
        if "app_name" not in kwargs["params"]:
            kwargs["params"]["app_name"] = self.app_name

        return self.request("GET", url, **kwargs).json()

    def get_redirect_url(self, uri: str):
        result = self.request("HEAD", uri, allow_redirects=True)
        return result.url

    def request(self, method: str, url: str, **kwargs) -> Response:
        prefix = f"{self.host_address}/v1/"
        uri = url.replace(prefix, "")
        if "https://" not in uri:
            url = f"{prefix}{uri}"

        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response
