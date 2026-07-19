class AppException(Exception):
    """Base application exception."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ResourceNotFoundException(AppException):
    """Raised when a resource is not found."""


class DuplicateResourceException(AppException):
    """Raised when a duplicate resource exists."""


class ValidationException(AppException):
    """Raised when business validation fails."""