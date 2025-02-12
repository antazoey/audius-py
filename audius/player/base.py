from abc import abstractmethod
from typing import TYPE_CHECKING

from audius.client import API

if TYPE_CHECKING:
    from audius.sdk import Audius
    from audius.types import PlayerType


class BasePlayer(API):
    def __init__(self, player_type: "PlayerType", sdk: "Audius"):
        self._type = player_type
        super().__init__(sdk)

    @abstractmethod
    def is_available(self) -> bool:
        """
        Returns True if this play is working.
        """

    @abstractmethod
    def play(self, url: str):
        """
        Stream and play track from Audius.
        Player-subclasses must implement this method.
        """

    def display_now_playing(self, track: dict):
        print(
            f"({self._type.value.lower().capitalize()}) "
            f"Now playing '{track['title']}' by {track['user']['name']}"
        )
