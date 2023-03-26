from typing import Type

import click

from audius.cli.utils import sdk


def config(sdk_cls: Type):
    sdk.py = sdk_cls

    @click.group(name="config")
    def cli():
        """
        Show configuration.
        """

    @cli.command()
    @sdk.audius()
    def app_name(sdk):
        """
        Show the app name.
        """

        click.echo(sdk.config.app_name)

    return cli
