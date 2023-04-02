import os
from typing import Dict, Optional, Union

from audius.player import PlayerType

DEFAULT_APP_NAME = "audius-py"
AUDIUS_APP_NAME_ENV_VAR = "AUDIUS_APP_NAME"
AUDIUS_HOST_NAME_ENV_VAR = "AUDIUS_HOST_NAME"
AUDIUS_PLAYER_ENV_VAR = "AUDIUS_PLAYER"


class Config:
    """
    Base class for configuring the Audius SDK.
    """

    def __init__(
        self,
        app_name: str = DEFAULT_APP_NAME,
        host: Optional[str] = None,
        aliases: Optional[Dict[str, str]] = None,
        player: Optional[Union[PlayerType, str]] = None,
    ):
        self.app_name = app_name
        self.host = host  # Uses random if not provided.
        self.aliases = aliases or {}
        self.player = PlayerType(player) if player is not None else None

    @classmethod
    def from_env(cls) -> "Config":
        app_name = os.environ.get(AUDIUS_APP_NAME_ENV_VAR, DEFAULT_APP_NAME)
        host = os.environ.get(AUDIUS_HOST_NAME_ENV_VAR)
        player = os.environ.get(AUDIUS_PLAYER_ENV_VAR)
        return cls(app_name=app_name, host=host, player=player)
