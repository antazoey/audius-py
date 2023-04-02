from typing import TYPE_CHECKING, Dict, Optional, Type

from audius.client import API
from audius.exceptions import MissingPlayerError
from audius.player.af import AFPlayer
from audius.player.base import BasePlayer
from audius.player.vlc import VLCPlayer
from audius.types import PlayerType

if TYPE_CHECKING:
    from audius.sdk import Audius


class Player(API):
    def __init__(self, sdk: "Audius") -> None:
        super().__init__(sdk)
        self._player_classes: Dict[PlayerType, Type] = {
            PlayerType.AFPLAY: AFPlayer,
            PlayerType.VLC: VLCPlayer,
        }
        self._player_map: Dict[PlayerType, BasePlayer] = {}

    def play(self, url: str, player_type: Optional[PlayerType] = None):
        player = self.get_player(player_type=player_type)
        player.play(url)

    def display_now_playing(self, track: Dict, player_type: Optional[PlayerType] = None):
        player = self.get_player(player_type=player_type)
        player.display_now_playing(track)

    def get_player(self, player_type: Optional[PlayerType] = None) -> BasePlayer:
        player_type = player_type or self.config.player
        if player_type is not None:
            if player_type not in self._player_classes:
                raise ValueError(f"Unknown player type '{player_type}'")

            self._player_map[player_type] = self._player_classes[player_type](self.sdk)
            return self._player_map[player_type]

        if self._player_map:
            # Use previously connected player.
            player_type = next(iter(self._player_map))
            return self._player_map[player_type]

        # Find an available player.
        for player_cls in self._player_classes.values():
            player = player_cls(self.sdk)
            if player.is_available():
                self._player_map[player._type] = player
                return player

        raise MissingPlayerError()
