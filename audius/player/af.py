import os
import subprocess
import tempfile
import threading
import time
from typing import TYPE_CHECKING

from audius.player.base import BasePlayer
from audius.types import PlayerType

if TYPE_CHECKING:
    from audius.sdk import Audius


class AFPlayer(BasePlayer):
    def __init__(self, sdk: "Audius"):
        super().__init__(PlayerType.AFPLAY, sdk)

    def is_available(self):
        try:
            subprocess.run("afplay", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except FileNotFoundError:
            return False

    def play(self, url: str):
        download_url = self.client.get_redirect_url(url)
        with tempfile.NamedTemporaryFile(mode="w+b", delete=False) as _file:
            fd3 = os.dup(_file.fileno())

            def download():
                self.sdk.tracks.download(download_url, fd3, hide_output=True)

            # Stream the song while playing it to prevent waiting
            # for entire track to finish download.
            thread = threading.Thread(target=download)
            thread.start()
            time.sleep(5)  # Buffer
            subprocess.Popen(["afplay", _file.name])
            thread.join()
            time.sleep(1)
