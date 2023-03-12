from pathlib import Path

import click

from audius.cli.utils import audius_sdk


@click.group()
def tracks():
    """
    Browse and listen to tracks.
    """


@tracks.command()
@audius_sdk()
def trending(sdk):
    """
    Page through trending tracks.
    """

    trending = list(sdk.tracks.trending())
    gen = (f"{i + 1}: {x['track_name']} (id={x['id']})\n" for i, x in enumerate(trending))
    click.echo_via_pager(gen)


@tracks.command()
@audius_sdk()
@click.argument("track_id")
def get(sdk, track_id):
    """
    Get a track.
    """

    track = sdk.tracks.get(track_id)
    _echo_track(track)


@tracks.command()
@audius_sdk()
@click.argument("query")
def search(sdk, query):
    """
    Search through tracks.
    """

    result = sdk.tracks.search(query=query)
    for idx, track in enumerate(result):
        _echo_track(track)

        if idx < len(result) - 1:
            click.echo()


@tracks.command()
@audius_sdk()
@click.argument("track_id")
def play(sdk, track_id):
    """
    Play a track.
    """

    sdk.tracks.play(track_id)


@tracks.command()
@audius_sdk()
@click.argument("track_id")
@click.argument("out_path", type=Path)
def download(sdk, track_id, out_path):
    """
    Download a track.
    """

    sdk.tracks.download(track_id, out_path)


def _echo_track(track: dict):
    click.echo(f"Track {track['title']} (id={track['id']})")
    click.echo(f"Description: {track['description']}")
    click.echo(f"Artist: {track['user']['name']}")
    click.echo(f"Genre: {track['genre']}, Mood: {track['mood']}")
    click.echo(f"Duration: {track['duration']}")
