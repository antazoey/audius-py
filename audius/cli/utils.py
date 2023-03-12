import os

import click

from audius.exceptions import UnknownAppError
from audius.sdk import AUDIUS_APP_NAME_ENV_VAR
from audius.sdk import Audius as BaseAudius


def audius_sdk():
    """
    A click command decorator giving you access to the SDK.
    """

    class Audius(BaseAudius):
        def __init__(self):
            value = os.environ.get(AUDIUS_APP_NAME_ENV_VAR)
            if not value:
                raise UnknownAppError()

            super().__init__(value)

    def decorator(f):
        f = click.make_pass_decorator(Audius, ensure=True)(f)
        return f

    return decorator
