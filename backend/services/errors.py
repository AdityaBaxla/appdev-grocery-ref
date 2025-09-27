class ServiceError(Exception):
    """Base class for service-related errors."""

class InvalidInputError(ServiceError):
    pass

class InvalidEmailError(ServiceError):
    pass

class WrongPasswordError(ServiceError):
    pass

class ForeignKeyConstraintError(ServiceError):
    def __init__(self, message = "Invalid foreign key", *args: object) -> None:
        super().__init__(message)
