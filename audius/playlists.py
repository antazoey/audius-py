from typing import Dict, Iterator, List, Optional

from requests.exceptions import HTTPError

from audius.client import API
from audius.exceptions import PlaylistNotFoundError


class Playlists(API):
    def trending(self) -> Iterator[dict]:
        yield from self.client.get("playlists/trending").get("data", [])

    def get(self, playlist_id: str):
        playlist_id = self._handle_id(playlist_id)
        try:
            result = self.client.get(f"playlists/{playlist_id}")
        except HTTPError as err:
            if err.response.status_code == 404:
                raise PlaylistNotFoundError(playlist_id)

            raise

        return result.get("data", {})

    def search(self, query: Optional[str] = None) -> List[Dict]:
        result = self.client.get("playlists/search", params={"query": query})
        return result.get("data", [])
