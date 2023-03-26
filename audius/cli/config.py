import click

from audius.cli.utils import sdk


@click.group()
def config():
    """
    Show configuration.
    """


@config.command()
@sdk.audius()
def app_name(sdk):
    """
    Show the app name.
    """

    click.echo(sdk.config.app_name)
