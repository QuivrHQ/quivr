class NodeValidationError(Exception):
    """Raised when node state validation fails."""

    pass


class NodeExecutionError(Exception):
    """Raised when node execution fails."""

    pass


class ConfigExtractionError(Exception):
    """Raised when config extraction fails."""

    pass
