class ServiceError(Exception):
    """Base class for service-related errors."""

class InvalidInputError(ServiceError):
    pass

class InvalidEmailError(ServiceError):
    pass

class WrongPasswordError(ServiceError):
    pass
