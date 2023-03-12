from functools import cached_property

from requests import Session


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

        url = f"{self.host_address}/v1/{url}"
        return self.request("GET", url, **kwargs)

    def request(self, method: str, url: str, **kwargs) -> dict:
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
