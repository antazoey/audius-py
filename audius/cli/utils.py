import click

from audius.sdk import Audius


def audius_sdk():
    """
    A click command decorator giving you access to the SDK.
    """

    def decorator(f):
        f = click.make_pass_decorator(Audius, ensure=True)(f)
        return f

    return decorator
