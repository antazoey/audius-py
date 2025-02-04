from typing import Optional

from cyclopts import App

from audius import Audius
from audius.cli.config import config
from audius.cli.playlists import playlists
from audius.cli.tips import tips
from audius.cli.tracks import tracks
from audius.cli.users import users
from audius.cli.utils import print
from audius.client_factory import get_hosts
from audius.types import PlayerType

audius = App()
audius.command(config)
audius.command(playlists)
audius.command(tips)
audius.command(tracks)
audius.command(users)


@audius.command
def hosts():
    """
    List available hosts
    """
    all_hosts = list(get_hosts())
    for host in all_hosts:
        print(host)


@audius.command
def play(track_id: Optional[str] = None, player: Optional[PlayerType] = None):
    """
    Play something from Audius
    """
    sdk = Audius()
    sdk.tracks.play(track_id, player=player)
