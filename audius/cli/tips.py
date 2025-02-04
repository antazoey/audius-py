from typing import Optional

from cyclopts import App

from audius.cli.utils import print
from audius.sdk import Audius

tips = App(name="tips", help="View tips")


@tips.command
def get(
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    user_id: Optional[str] = None,
    receiver_min_followers: Optional[int] = None,
    receiver_is_verified: bool = False,
    current_user_follows: Optional[str] = None,
    unique_by: Optional[str] = None,
) -> None:
    """
    Get tips

    Args:
        offset (int | None): Number of tips to skip
        limit (int | None): Number of tips to fetch
        user_id (str | None): User ID
        receiver_min_followers (int | None): Exclude recipients without min followers
        receiver_is_verified (bool): Exclude non-verified recipients
        current_user_follows (str | None): Query by who recipient follows
        unique_by (str | None): Require involvement in the given capacity
    """
    sdk = Audius()
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
        print("No tips found.")

    else:
        for idx, tip in enumerate(result):
            print(
                f"'{tip['sender']['name']}' tipped '{tip['amount']}' "
                f"to '{tip['receiver']['name']}' on '{tip['created_at']}'."
            )
