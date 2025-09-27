class ResourceError(Exception):
    """base error for resource based errors"""

class InvalidDataError(ResourceError):
    def __init__(self, message = "invalid/improper data"):
        super().__init__(message)