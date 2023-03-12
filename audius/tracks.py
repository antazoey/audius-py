from pathlib import Path
from typing import Dict, Iterator, List, Optional

import click
from requests.exceptions import HTTPError
from tqdm import tqdm  # type: ignore

from audius.client import API, Client
from audius.exceptions import OutputPathError, TrackNotFoundError
from audius.player import Player


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


class Tracks(API):
    def __init__(self, client: Client, player: Player):
        self.player = player
        super().__init__(client)

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

    def play(self, track_id: str):
        track = self.get(track_id)
        url = f"{self.client.host_address}/v1/tracks/{track_id}/stream"
        click.echo(f"Now playing '{track['title']}' by {track['user']['name']}")
        self.player.play(url)

    def download(self, track_id: str, output_path: Path):
        if output_path.is_file():
            raise OutputPathError("File exists.")

        track = self.get(track_id)
        click.echo(f"Downloading '{track['title']}' by {track['user']['name']}")
        click.echo(f"Saving at '{output_path}'.")

        uri = f"tracks/{track_id}/stream"
        headers = {"Accept": "application/octet-stream"}
        response = self.client.request("GET", uri, stream=True, headers=headers)
        with DownloadProgressBar(
            unit="B", unit_scale=True, miniters=1, desc=uri.split("/")[-1]
        ) as bar:
            with open(str(output_path), "wb") as out_file:
                for chunk in response.iter_content(chunk_size=1, decode_unicode=True):
                    if chunk:
                        out_file.write(chunk)
                        bar.update(len(chunk))
