import click

from audius.sdk import sdk


@click.group()
def audius():
    pass


@audius.command()
def hosts():
    """
    List available hosts.
    """

    gen = (f"{x}\n" for x in sdk.get_hosts())
    click.echo_via_pager(gen)
