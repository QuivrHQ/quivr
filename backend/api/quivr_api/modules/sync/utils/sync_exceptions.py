class SyncException(Exception):
    def __init__(self, message="A sync-related error occurred"):
        self.message = message
        super().__init__(self.message)


class SyncCreationError(SyncException):
    def __init__(self, message="An error occurred while creating"):
        super().__init__(message)


class SyncUpdateError(SyncException):
    def __init__(self, message="An error occurred while updating"):
        super().__init__(message)


class SyncDeleteError(SyncException):
    def __init__(self, message="An error occurred while deleting"):
        super().__init__(message)


class SyncEmptyCredentials(SyncException):
    def __init__(
        self, message="You do not have credentials to access files from this sync."
    ):
        super().__init__(message)


class SyncNotFoundException(SyncException):
    def __init__(self, message="The requested sync was not found"):
        super().__init__(message)
