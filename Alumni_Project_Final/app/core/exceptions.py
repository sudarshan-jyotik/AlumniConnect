"""
Custom exception classes for AlumniConnect.
"""


class AppException(Exception):
    """Base exception for application errors."""
    
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundException(AppException):
    """Exception raised when a resource is not found."""
    
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)


class UnauthorizedException(AppException):
    """Exception raised for unauthorized access."""
    
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, status_code=401)


class ForbiddenException(AppException):
    """Exception raised for forbidden access."""
    
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, status_code=403)


class ValidationException(AppException):
    """Exception raised for validation errors."""
    
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, status_code=422)


class ConflictException(AppException):
    """Exception raised for resource conflicts."""
    
    def __init__(self, message: str = "Resource conflict"):
        super().__init__(message, status_code=409)
