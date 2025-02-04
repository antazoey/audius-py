from pathlib import Path
from typing import Optional

from cyclopts import App

from audius.cli.utils import print
from audius.const import DEFAULT_BUFFER_SIZE
from audius.sdk import Audius
from audius.types import PlayerType

tracks = App(name="tracks", help="View and play tracks")


@tracks.command
def trending(top: int = 10):
    """
    Show trending tracks

    Args:
        top (int): The number to show
    """
    sdk = Audius()
    count = 0
    for track in sdk.tracks.trending():
        print(f"{track['title']} (id={track['id']})")
        count += 1
        if count >= top:
            break


@tracks.command
def get(track_id: str):
    """
    Get a track

    Args:
        track_id (str): The track ID
    """
    sdk = Audius()
    track = sdk.tracks.get(track_id)
    print_track(track)


@tracks.command
def search(query: str = ""):
    """
    Search tracks

    Args:
        query (str): The search query
    """
    sdk = Audius()
    result = sdk.tracks.search(query=query)
    for idx, track in enumerate(result):
        print_track(track)
        if idx < len(result) - 1:
            print()


@tracks.command(name="play")
def play_track(track_id: Optional[str] = None, player: Optional[PlayerType] = None):
    """
    Play a track

    Args:
        track_id (str | None): The track ID, defaults to random
        player (str | None): The player name, such as 'afplay' or 'vlc'
    """
    sdk = Audius()
    sdk.tracks.play(track_id, player=player)


@tracks.command
def download(track_id: str, out_path: Path, buffer_size: int = DEFAULT_BUFFER_SIZE):
    """
    Download a track

    Args:
        track_id (str): The track ID
        out_path (Path): The output path
        buffer_size (int): The buffer size, defaults to 1,048,576
    """
    sdk = Audius()
    sdk.tracks.download(track_id, out_path, chunk_size=buffer_size)


def print_track(track: dict):
    print(f"Track {track['title']} (id={track['id']})")
    print(f"Description: {track['description']}")
    print(f"Artist: {track['user']['name']}")
    print(f"Genre: {track['genre']}, Mood: {track['mood']}")
    print(f"Duration: {track['duration']}")
