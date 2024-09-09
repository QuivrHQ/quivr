class KnowledgeException(Exception):
    def __init__(self, message="A knowledge-related error occurred"):
        self.message = message
        super().__init__(self.message)


class UploadError(KnowledgeException):
    def __init__(self, message="An error occurred while uploading"):
        super().__init__(message)


class CreationError(KnowledgeException):
    def __init__(self, message="An error occurred while creating"):
        super().__init__(message)


class UpdateError(KnowledgeException):
    def __init__(self, message="An error occurred while updating"):
        super().__init__(message)


class DeleteError(KnowledgeException):
    def __init__(self, message="An error occurred while deleting"):
        super().__init__(message)
