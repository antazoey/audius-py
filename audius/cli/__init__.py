import difflib
import re
from typing import Any

import click

from audius.cli.config import config
from audius.cli.playlists import playlists
from audius.cli.tips import tips
from audius.cli.tracks import tracks
from audius.cli.users import users
from audius.client_factory import get_hosts
from audius.exceptions import AudiusException
from audius.sdk import Audius


class AudiusCLI(click.Group):
    def invoke(self, ctx) -> Any:
        try:
            return super().invoke(ctx)
        except click.UsageError as err:
            self._suggest_cmd(err)
        except AudiusException as err:
            raise click.ClickException(f"({type(err).__name__}) {err}") from err

    @staticmethod
    def _suggest_cmd(usage_error):
        if usage_error.message is None:
            raise usage_error

        match = re.match("No such command '(.*)'.", usage_error.message)
        if not match:
            raise usage_error

        bad_arg = match.groups()[0]
        suggested_commands = difflib.get_close_matches(
            bad_arg, list(usage_error.ctx.command.commands.keys()), cutoff=0.6
        )
        if suggested_commands:
            if bad_arg not in suggested_commands:
                usage_error.message = (
                    f"No such command '{bad_arg}'. Did you mean {' or '.join(suggested_commands)}?"
                )

        raise usage_error


def create_cli(sdk_cls=Audius):
    @click.group(cls=AudiusCLI)
    def cli():
        "Audius CLI"

    @cli.command()
    def hosts():
        """
        List available hosts.
        """

        gen = (f"{x}\n" for x in get_hosts())
        click.echo_via_pager(gen)

    cli.add_command(users(sdk_cls))
    cli.add_command(playlists(sdk_cls))
    cli.add_command(tracks(sdk_cls))
    cli.add_command(tips(sdk_cls))
    cli.add_command(config(sdk_cls))

    return cli


audius = create_cli()
