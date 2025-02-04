from cyclopts import App

from audius.cli.utils import print
from audius.sdk import Audius

config = App(name="config", help="Manage config")


@config.command
def app_name():
    """
    Show the application name
    """
    sdk = Audius()
    print(sdk.config.app_name)
