from functools import cached_property

from requests import Response, Session


class API:
    def __init__(self, client: "Client"):
        self.client = client


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

    def request(self, method: str, url: str, **kwargs) -> Response:
        url = f"{self.host_address}/v1/{url}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response
