from typing import Dict, Iterator, Optional

from requests.exceptions import HTTPError

from audius.client import Client
from audius.exceptions import UserNotFoundError


class Users:
    def __init__(self, app_name: str, client: Client):
        self.app_name = app_name
        self.client = client

    def top(self) -> Iterator[dict]:
        yield from self.client.get("users/top").get("data", [])

    def get(self, user_id: str) -> Dict:
        try:
            result = self.client.get(f"users/{user_id}")
        except HTTPError as err:
            if err.response.status_code == 404:
                raise UserNotFoundError(user_id)

            raise

        return result.get("data", {})

    def search(self, query: Optional[str] = None):
        return self.client.get("users/search", params={"query": query}).get("data")
