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
