from typing import Type

import click

from audius.cli.utils import sdk


def tips(sdk_cls: Type):
    sdk.py = sdk_cls

    @click.group(name="tips")
    def cli():
        """
        Checkout artist tips.
        """

    @cli.command()
    @sdk.audius()
    @click.option("--offset", help="Number of tips to skip (for pagination).", type=int)
    @click.option("--limit", help="Number of tips to fetch.", type=int)
    @click.option("--user-id", help="The user making the request.")
    @click.option(
        "--receiver-min-followers", help="Exclude recipients without min followers.", type=int
    )
    @click.option("--receiver-is-verified", help="Exclude non-verified recipients.", is_flag=True)
    @click.option("--current-user-follows", help="Query by who recipient follows.")
    @click.option("--unique-by", help="Require involvement in the given capacity.")
    def get(
        sdk,
        offset,
        limit,
        user_id,
        receiver_min_followers,
        receiver_is_verified,
        current_user_follows,
        unique_by,
    ):
        """
        Get tips.
        """

        result = sdk.tips.get(
            offset=offset,
            limit=limit,
            user_id=user_id,
            receiver_min_followers=receiver_min_followers,
            receiver_is_verified=receiver_is_verified,
            current_user_follows=current_user_follows,
            unique_by=unique_by,
        )
        if not result:
            click.echo("No tips found.")

        else:
            for idx, tip in enumerate(result):
                click.echo(
                    f"'{tip['sender']['name']}' tipped '{tip['amount']}' "
                    f"to '{tip['receiver']['name']}' on '{tip['created_at']}'."
                )

    return cli
