from typing import Type

import click

from audius.cli.utils import sdk


def users(sdk_cls: Type):
    sdk.py = sdk_cls

    @click.group(name="users")
    def users():
        """
        Commands for users.
        """

    @users.command()
    @sdk.audius()
    def top(sdk):
        """
        Page through the top users.
        """

        top = list(sdk.users.top())
        gen = (f"{i + 1}: {x['name']} (id={x['id']})\n" for i, x in enumerate(top))
        click.echo_via_pager(gen)

    @users.command()
    @sdk.audius()
    @click.argument("user_id")
    def get(sdk, user_id):
        """
        Get a user.
        """

        user = sdk.users.get(user_id)
        _echo_user(user)

    @users.command()
    @sdk.audius()
    @click.argument("query")
    def search(sdk, query):
        """
        Search for users.
        """

        result = sdk.users.search(query=query)
        for idx, user in enumerate(result):
            _echo_user(user)

            if idx < len(result) - 1:
                click.echo()

    @users.command()
    @sdk.audius()
    @click.argument("user_id")
    def wallets(sdk, user_id):
        """
        List user wallet addresses.
        """

        result = sdk.users.get_connected_wallets(user_id)
        if result["erc_wallets"]:
            click.echo("ERC Wallets:")
            for addr in result["erc_wallets"]:
                click.echo(f"\t{addr}")

        else:
            click.echo("No ERC wallets")

        if result["spl_wallets"]:
            # Newline sep.
            click.echo()
            click.echo("SPL Wallets:")
            for addr in result["spl_wallets"]:
                click.echo(addr)

    @users.command()
    @sdk.audius()
    @click.argument("user_id")
    def tracks(sdk, user_id):
        """
        Get a user's tracks.
        """

        tracks = sdk.users.get_tracks(user_id)
        for idx, track in enumerate(tracks):
            click.echo(f"Track: {track['title']} (id={track['id']})")

            if idx < len(tracks) - 1:
                click.echo()

    return users


def _echo_user(user: dict):
    click.echo(f"Artist: {user['name']} (id={user['id']})")
    click.echo(f"Bio: {user['bio']}")
    click.echo(f"Followers: {user['follower_count']}, Followees: {user['followee_count']}")
    click.echo(f"ERC Wallet: {user['erc_wallet']}, SPL Wallet: {user['spl_wallet']}")
