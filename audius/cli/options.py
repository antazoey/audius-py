import click

from audius.types import PlayerType


def player_option():
    return click.option(
        "--player",
        help="The player to use.",
        type=click.Choice([x.value for x in PlayerType.__members__.values()], case_sensitive=False),
        callback=lambda _, _2, val: PlayerType(val) if val else None,
    )
