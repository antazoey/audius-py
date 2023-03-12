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
    user = sdk.users.get(user_id)
    _echo_user(user)


@users.command()
@click.option("--query", help="A user query.")
def search(query):
    sdk = Audius.from_env()
    result = sdk.users.search(query=query)
    for idx, user in enumerate(result):
        _echo_user(user)

        if idx < len(result) - 1:
            click.echo()


def _echo_user(user: dict):
    click.echo(f"Artist: {user['name']} (id={user['id']})")
    click.echo(f"Bio: {user['bio']}")
    click.echo(f"Followers: {user['follower_count']}, Followees: {user['followee_count']}")
    click.echo(f"ERC Wallet: {user['erc_wallet']}, SPL Wallet: {user['spl_wallet']}")

