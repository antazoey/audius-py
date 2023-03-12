import click

from audius.sdk import Audius


@click.group()
def users():
    """
    Commands for users.
    """


@users.command()
def top():
    """
    Page through the top users.
    """

    sdk = Audius.from_env()
    top = list(sdk.users.top())
    gen = (f"{i + 1}: {x['name']} (id={x['id']})\n" for i, x in enumerate(top))
    click.echo_via_pager(gen)


@users.command()
@click.argument("user_id")
def get(user_id):
    """
    Get a user.
    """

    sdk = Audius.from_env()
    artist = sdk.users.get(user_id)
    click.echo(f"Artist: {artist['name']}")
    click.echo(f"Bio: {artist['bio']}")
    click.echo(f"Followers: {artist['follower_count']}, Followees: {artist['followee_count']}")
    click.echo(f"ERC Wallet: {artist['erc_wallet']}, SPL Wallet: {artist['spl_wallet']}")
