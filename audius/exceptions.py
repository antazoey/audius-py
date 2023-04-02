class AudiusException(Exception):
    """
    An exception raised by the Audius SDK.
    """


class UnknownAppError(AudiusException):
    """
    Raised when the app name is not known.
    Audius requires all API users to set an app name.
    """

    def __init__(self):
        super().__init__("Unknown app. " "Try setting environment variable AUDIUS_APP_NAME.")


class UserNotFoundError(AudiusException):
    """
    Raised when a user is not found.
    """

    def __init__(self, user_id: str):
        self.user_id = user_id
        super().__init__(f"User '{user_id}' is not found.")


class PlaylistNotFoundError(AudiusException):
    """
    Raised when a playlist is not found.
    """

    def __init__(self, playlist_id: str):
        self.playlist_id = playlist_id
        super().__init__(f"Playlist '{playlist_id}' is not found.")


class TrackNotFoundError(AudiusException):
    """
    Raised when a track is not found.
    """

    def __init__(self, track_id: str):
        self.track_id = track_id
        super().__init__(f"Track '{track_id}' is not found.")


class MissingPlayerError(AudiusException):
    """
    Raised when no player configured to stream tracks.
    """

    def __init__(self):
        super().__init__("Missing audio player. Try installing VLC music player.")


class OutputPathError(AudiusException):
    """
    Raise when there is an issue with an output path.
    """
