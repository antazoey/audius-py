import click

from audius.cli.utils import audius_sdk


@click.group()
def playlists():
    """
    Manage playlists.
    """


@playlists.command()
@audius_sdk()
@click.argument("playlist_id")
def get(sdk, playlist_id):
    """
    Get a playlist.
    """

    playlist = sdk.playlists.get(playlist_id)
    click.echo(playlist)
