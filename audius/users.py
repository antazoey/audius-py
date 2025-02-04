from collections.abc import Iterator

from requests.exceptions import HTTPError

from audius.client import API
from audius.exceptions import UserNotFoundError


class Users(API):
    def top(self) -> Iterator[dict]:
        yield from self.client.get("users/top").get("data", [])

    def get(self, user_id: str) -> dict:
        user_id = self._handle_id(user_id)
        try:
            result = self.client.get(f"users/{user_id}")
        except HTTPError as err:
            if err.response.status_code == 404:
                raise UserNotFoundError(user_id)

            raise

        return result.get("data", {})

    def search(self, query: str = "") -> list[dict]:
        result = self.client.get("users/search", params={"query": query})
        return result.get("data", [])

    def get_connected_wallets(self, user_id: str) -> dict:
        user_id = self._handle_id(user_id)
        result = self.client.get(f"users/{user_id}/connected_wallets")
        return result.get("data", {})

    def get_tracks(self, user_id: str) -> list[dict]:
        user_id = self._handle_id(user_id)
        result = self.client.get(f"users/{user_id}/tracks")
        return result.get("data", [])
