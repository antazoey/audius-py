from enum import Enum
from pathlib import Path
from typing import IO, Union


class PlayerType(Enum):
    VLC = "VLC"
    AFPLAY = "AFPLAY"


FileDestination = Union[Path, IO, int]
"""File path, an open file stream, or a file descriptor."""
