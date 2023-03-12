import click

from audius.cli.utils import audius_sdk


@click.group()
def playlists():
    """
    Manage playlists.
    """


@playlists.command()
@audius_sdk()
def trending(sdk):
    """
    Page through trending playlists.
    """

    trending = list(sdk.playlists.trending())
    gen = (f"{i + 1}: {x['playlist_name']} (id={x['id']})\n" for i, x in enumerate(trending))
    click.echo_via_pager(gen)


@playlists.command()
@audius_sdk()
@click.argument("playlist_id")
def get(sdk, playlist_id):
    """
    Get a playlist.
    """

    playlist = sdk.playlists.get(playlist_id)
    _echo_playlist(playlist)


@playlists.command()
@audius_sdk()
@click.argument("query")
def search(sdk, query):
    """
    Search through playlists.
    """

    result = sdk.playlists.search(query=query)
    for idx, playlist in enumerate(result):
        _echo_playlist(playlist)

        if idx < len(result) - 1:
            click.echo()


def _echo_playlist(playlist: dict):
    click.echo(f"Playlist: {playlist['playlist_name']} (id={playlist['id']})")
    click.echo(f"Description: {playlist['description']}")
    click.echo(f"User: {playlist['user']['name']} (id={playlist['user']['id']})")
    click.echo(f"Total plays: {playlist['total_play_count']}")
