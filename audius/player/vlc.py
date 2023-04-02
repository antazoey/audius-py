import time
from functools import cached_property
from typing import TYPE_CHECKING

from audius.exceptions import MissingPlayerError
from audius.player.base import BasePlayer
from audius.types import PlayerType

if TYPE_CHECKING:
    from audius.sdk import Audius


class VLCPlayer(BasePlayer):
    def __init__(self, sdk: "Audius"):
        super().__init__(PlayerType.VLC, sdk)

    @cached_property
    def vlc(self):
        # Lazy load to allow SDK to work when VLC not installed.
        try:
            import vlc  # type: ignore

        except Exception:
            raise MissingPlayerError()

        return vlc

    @cached_property
    def _player(self):
        return self.vlc.MediaPlayer()

    def is_available(self) -> bool:
        try:
            _ = self.vlc
            return True
        except MissingPlayerError:
            return False

    def play(self, url: str):
        media = self.vlc.Media(url)
        self._player.set_media(media)
        self._player.play()
        time.sleep(5)  # Wait 5 seconds for it to start.
        while self._player.is_playing():
            time.sleep(1)
