from pathlib import Path
from typing import Type

import click

from audius.cli.options import player_option
from audius.cli.utils import sdk

DEFAULT_BUFFER_SIZE = 1024 * 1024


def tracks(sdk_cls: Type):
    sdk.py = sdk_cls

    @click.group(name="tracks")
    def cli():
        """
        Browse and listen to tracks.
        """

    @cli.command()
    @sdk.audius()
    def trending(sdk):
        """
        Page through trending tracks.
        """

        trending = list(sdk.tracks.trending())
        gen = (f"{i + 1}: {x['track_name']} (id={x['id']})\n" for i, x in enumerate(trending))
        click.echo_via_pager(gen)

    @cli.command()
    @sdk.audius()
    @click.argument("track_id")
    def get(sdk, track_id):
        """
        Get a track.
        """

        track = sdk.tracks.get(track_id)
        _echo_track(track)

    @cli.command()
    @sdk.audius()
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

    @cli.command()
    @sdk.audius()
    @click.argument("track_id")
    @player_option()
    def play(sdk, track_id, player):
        """
        Play a track.
        """

        sdk.tracks.play(track_id, player=player)

    @cli.command()
    @sdk.audius()
    @click.argument("track_id")
    @click.argument("out_path", type=Path)
    @click.option(
        "--buffer-size", help="The buffer size when downloading.", default=DEFAULT_BUFFER_SIZE
    )
    def download(sdk, track_id, out_path, buffer_size):
        """
        Download a track.
        """

        sdk.tracks.download(track_id, out_path, chunk_size=buffer_size)

    return cli


def _echo_track(track: dict):
    click.echo(f"Track {track['title']} (id={track['id']})")
    click.echo(f"Description: {track['description']}")
    click.echo(f"Artist: {track['user']['name']}")
    click.echo(f"Genre: {track['genre']}, Mood: {track['mood']}")
    click.echo(f"Duration: {track['duration']}")
