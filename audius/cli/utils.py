import click

from audius.sdk import Audius


class sdk:
    py = Audius

    @classmethod
    def audius(cls):
        """
        A click command decorator giving you access to the SDK.
        """

        def decorator(f):
            f = click.make_pass_decorator(cls.py, ensure=True)(f)
            return f

        return decorator
