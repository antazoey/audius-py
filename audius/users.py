from typing import Dict, Iterator

from requests.exceptions import HTTPError

from audius.client import Client
from audius.exceptions import UserNotFoundError


class Users:
    def __init__(self, app_name: str, client: Client):
        self.app_name = app_name
        self.client = client

    def top(self) -> Iterator[dict]:
        params = {"app_name": self.app_name}
        yield from self.client.get("users/top").get("data", [])

    def get(self, user_id: str) -> Dict:
        params = {"app_name": self.app_name}

        try:
            result = self.client.get(f"users/{user_id}", params=params)
        except HTTPError as err:
            if err.response.status_code == 404:
                raise UserNotFoundError(user_id)

            raise

        return result.get("data", {})
