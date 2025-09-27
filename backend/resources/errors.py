class ResourceError(Exception):
    """base error for resource based errors"""

class InvalidDataError(ResourceError):
    pass