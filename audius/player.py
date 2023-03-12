import time
from functools import cached_property

from audius.exceptions import MissingPlayerError


def get_vlc():
    try:
        import vlc  # type: ignore

    except Exception:
        raise MissingPlayerError()

    return vlc


class Player:
    @cached_property
    def vlc(self):
        # Lazy load to allow SDK to work when VLC not installed.
        return get_vlc()

    @cached_property
    def _player(self):
        return self.vlc.MediaPlayer()

    def play(self, url: str):
        media = self.vlc.Media(url)
        self._player.set_media(media)
        self._player.play()
        time.sleep(5)  # Wait 5 seconds for it to start.
        while self._player.is_playing():
            time.sleep(1)
