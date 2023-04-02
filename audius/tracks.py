import os
from pathlib import Path
from typing import IO, Dict, Iterable, Iterator, List, Optional, Tuple, Union

import click
from requests import Response
from requests.exceptions import HTTPError
from tqdm import tqdm  # type: ignore

from audius.client import API
from audius.exceptions import OutputPathError, TrackNotFoundError
from audius.types import FileDestination, PlayerType


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def _write_response(
    output_paths: List[FileDestination],
    response: Response,
    progress_bar: Optional[DownloadProgressBar] = None,
    chunk_size: int = 1,
):
    output_files: List[Tuple[IO, bool]] = []
    for output_path in output_paths:
        if isinstance(output_path, Path):
            _file = open(str(output_path), "wb")
            output_files.append((_file, True))
        else:
            output_files.append((output_path, False))  # type: ignore

    for chunk in response.iter_content(chunk_size=chunk_size, decode_unicode=True):
        if chunk:
            for out_file, _ in output_files:
                if isinstance(out_file, int):
                    # File descriptor.
                    os.write(out_file, chunk)
                else:
                    out_file.write(chunk)

            if progress_bar is not None:
                progress_bar.update(len(chunk))

    for out_file, do_close in output_files:
        if do_close:
            out_file.close()


def _validate_output_paths(
    output_paths: Union[FileDestination, Iterable[FileDestination]]
) -> List[FileDestination]:
    output_path_ls: List[FileDestination]
    if not isinstance(output_paths, (list, tuple)):
        output_path_ls = [output_paths]  # type: ignore
    else:
        output_path_ls = list(output_paths)

    for path in output_path_ls:
        if isinstance(path, Path) and path.is_file():
            raise OutputPathError("File exists.")

    return output_path_ls


class Tracks(API):
    def trending(self) -> Iterator[dict]:
        yield from self.client.get("tracks/trending").get("data", [])

    def get(self, track_id: str):
        track_id = self._handle_id(track_id)
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

    def play(self, track_id: str, player: Optional[PlayerType] = None):
        track_id = self._handle_id(track_id)
        track = self.get(track_id)
        self.sdk.player.display_now_playing(track, player_type=player)
        url = f"{self.client.host_address}/v1/tracks/{track_id}/stream"
        self.sdk.player.play(url, player_type=player)

    def download(
        self,
        track_id: str,
        output_paths: Union[FileDestination, Iterable[FileDestination]],
        hide_output: bool = False,
        chunk_size: int = 1,
    ):
        output_path_ls = _validate_output_paths(output_paths)
        track_id = self._handle_id(track_id)

        # Allow full-URLs as well, in case using a re-direct.
        uri = f"tracks/{track_id}/stream" if "https://" not in track_id else track_id

        headers = {"Accept": "application/octet-stream"}
        response = self.client.request("GET", uri, stream=True, headers=headers)
        if hide_output:
            _write_response(output_path_ls, response, chunk_size=chunk_size)
            return

        # Show progress in output.
        progress_bar = DownloadProgressBar(
            unit="B", unit_scale=True, miniters=1, desc=uri.split("/")[-1]
        )
        track = self.get(track_id)
        click.echo(f"Downloading '{track['title']}' by {track['user']['name']}")

        dest = ", ".join([str(x) for x in output_path_ls])
        click.echo(f"Saving at '{dest}'.")

        with progress_bar as bar:
            _write_response(output_path_ls, response, progress_bar=bar)
