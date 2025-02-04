from cyclopts import App

from audius.cli.utils import print
from audius.sdk import Audius

playlists = App(name="playlists", help="View playlists")


@playlists.command
def trending(top: int = 10):
    """
    Show top trending playlists

    Args:
        top (int): The number of playlists to show
    """
    sdk = Audius()
    count = 0
    for idx, trending_playlist in enumerate(sdk.playlists.trending()):
        print(f"{idx + 1}: {trending_playlist['playlist_name']} (id={trending_playlist['id']})")
        count += 1
        if count >= top:
            break


@playlists.command
def get(playlist_id: str):
    """
    Get a playlist

    Args:
        playlist_id (str): The playlist ID
    """
    sdk = Audius()
    playlist = sdk.playlists.get(playlist_id)
    print_playlist(playlist)


@playlists.command()
def search(query: str = ""):
    """
    Search through playlists

    Args:
        query (str): The search query
    """
    sdk = Audius()
    result = sdk.playlists.search(query=query)
    for idx, playlist in enumerate(result):
        print_playlist(playlist)

        if idx < len(result) - 1:
            print()


def print_playlist(playlist: dict):
    print(f"Playlist: {playlist['playlist_name']} (id={playlist['id']})")
    print(f"Description: {playlist['description']}")
    print(f"User: {playlist['user']['name']} (id={playlist['user']['id']})")
    print(f"Total plays: {playlist['total_play_count']}")
