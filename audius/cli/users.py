from cyclopts import App

from audius.cli.utils import print
from audius.sdk import Audius

users = App(name="users", help="View users")


@users.command(name="top")
def show_top(top: int = 10):
    """
    Show top users

    Args:
        top (int): Number of users to show
    """
    sdk = Audius()
    count = 0
    for user in sdk.users.top():
        print(user)
        count += 1
        if count >= top:
            break


@users.command
def get(user_id: str):
    """
    Get a user

    Args:
        user_id (str): User ID
    """
    sdk = Audius()
    user = sdk.users.get(user_id)
    print_user(user)


@users.command
def search(query: str = ""):
    """
    Search for users

    Args:
        query (str): Search query
    """
    sdk = Audius()
    result = sdk.users.search(query=query)
    for idx, user in enumerate(result):
        print_user(user)

        if idx < len(result) - 1:
            print()


@users.command
def wallets(user_id: str):
    """
    List user wallet addresses

    Args:
        user_id (str): User ID
    """
    sdk = Audius()
    result = sdk.users.get_connected_wallets(user_id)
    if result["erc_wallets"]:
        print("ERC Wallets:")
        for addr in result["erc_wallets"]:
            print(f"\t{addr}")

    else:
        print("No ERC wallets")

    if result["spl_wallets"]:
        # Newline sep.
        print("\nSPL Wallets:")
        for addr in result["spl_wallets"]:
            print(addr)


@users.command
def tracks(user_id: str):
    """
    Show user tracks

    Args:
        user_id (str): User ID
    """
    sdk = Audius()
    user_tracks = sdk.users.get_tracks(user_id)
    for idx, track in enumerate(user_tracks):
        print(f"Track: {track['title']} (id={track['id']})")

        if idx < len(user_tracks) - 1:
            print()


def print_user(user: dict):
    print(f"Artist: {user['name']} (id={user['id']})")
    print(f"Bio: {user['bio']}")
    print(f"Followers: {user['follower_count']}, Followees: {user['followee_count']}")
    print(f"ERC Wallet: {user['erc_wallet']}, SPL Wallet: {user['spl_wallet']}")
