from requests.exceptions import HTTPError

from audius.client import API
from audius.exceptions import PlaylistNotFoundError


class Playlists(API):
    def get(self, playlist_id: str):
        try:
            result = self.client.get(f"playlists/{playlist_id}")
        except HTTPError as err:
            if err.response.status_code == 404:
                raise PlaylistNotFoundError(playlist_id)

            raise

        return result.get("data", {})
