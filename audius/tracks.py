from typing import Dict, Iterator, List, Optional

from requests.exceptions import HTTPError

from audius.client import API
from audius.exceptions import TrackNotFoundError


class Tracks(API):
    def trending(self) -> Iterator[dict]:
        yield from self.client.get("tracks/trending").get("data", [])

    def get(self, track_id: str):
        try:
            result = self.client.get(f"tracks/{track_id}")
        except HTTPError as err:
            if err.response.status_code == 404:
                raise TrackNotFoundError(track_id)

            raise

        return result.get("data", {})

    def search(self, query: Optional[str] = None) -> List[Dict]:
        result = self.client.get("tracks/search", params={"query": query})
        return result.get("data", [])
